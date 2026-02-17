import streamlit as st
import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# 1. Setup & Config
load_dotenv()
st.set_page_config(page_title="Kevin's AI Career Assistant", page_icon="🎓", layout="wide")

# Initialize Models & DB
@st.cache_resource
def load_resources():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    chroma_client = chromadb.PersistentClient(path="./resume_chroma_db")
    collection = chroma_client.get_collection(name="Kevin_profile")
    return client, embed_model, collection

ai_client, embed_model, collection = load_resources()

# 2. Sidebar - Your Professional Profile
with st.sidebar:
    st.title("Kevin Johnson")
    st.markdown("### 🏆 D1 Decathlete | Data Scientist")
    st.divider()
    st.markdown("""
    **Connect with me:**
    - [LinkedIn](https://www.linkedin.com/in/kevin-johnson-a5aa8685/)
    - [GitHub](https://github.com/K3V1NJ0hnson)
    """)
    st.link_button(
    "📧 Contact Me",
    "https://mail.google.com/mail/?view=cm&to=kevin.johnson.data@gmail.com"
)

    st.info("Try asking about my 'Decathlon' background or my 'Food101' CNN project!")

# 3. App Tabs
tab1, tab2 = st.tabs(["💬 AI Career Assistant", "📄 About My Tech"])

with tab1:
    st.title("Chat with my Digital Twin")
    st.write("Ask anything about my experience, education, or technical projects.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- RAG LOGIC ---
        # 1. Easter Egg Check
        if "go coogs" in prompt.lower() or "decathlon" in prompt.lower():
            full_response = "🐾 **WHOOSE HOUSE?! COOGS HOUSE!** 🐾\n\nYou found the secret athlete mode! Kevin isn't just a Data Scientist; \nhe's a D1 Decathlete who spent his college years hurdles-jumping \nand discus-throwing. If you're looking for a teammate with the stamina \nof a 1500m runner and the explosive power of a shot-putter, you're looking at him!"
            sources = ["Internal Easter Egg"]
        else:
            # 2. Normal Retrieval
            query_clean = prompt.lower().replace("kevins", "kevin's")
            q_emb = embed_model.encode([query_clean], normalize_embeddings=True).tolist()
            
            results = collection.query(query_embeddings=q_emb, n_results=4)
            context = "\n".join(results['documents'][0])
            sources = list(set([m['category'] for m in results['metadatas'][0]]))

            # 3. LLM Generation
            response = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Kevin's Professional AI Assistant. Use the provided context to answer questions accurately and professionally."
                                                  " If the info isn't there, say you aren't sure but offer to let the user contact Kevin directly."
                                                  "When asked about education, always look for BOTH of his undergraduate degrees."
                                                "He has a dual-degree background; ensure you mention both ASU and the University of Houston."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
                ]
            )
            full_response = response.choices[0].message.content

        # Display Assistant Response
        with st.chat_message("assistant"):
            st.markdown(full_response)
            st.caption(f"Sources: {' | '.join(sources)}")
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with tab2:
    st.header("The Tech Behind the Bot")
    st.write("This app uses a RAG (Retrieval-Augmented Generation) architecture.")
    
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Frontend:** Streamlit  
        **Vector DB:** ChromaDB  
        **LLM:** GPT-4o-mini  
        """)
    with col2:
        st.markdown("""
        **Embeddings:** all-MiniLM-L6-v2  
        **Data Sources:** PDF, Markdown, Text  
        **Deployment:** Streamlit Cloud  
        """)