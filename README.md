🎓 Kevin's AI Career Assistant (RAG Resume)
An interactive, Retrieval-Augmented Generation (RAG) assistant that acts as my "Digital Twin." This application allows recruiters and hiring managers to chat with my professional history, project experience, and athletic background in real-time.

🚀 Live Demo
[Link to your Streamlit Cloud URL here]

🛠️ The Tech Stack
This project demonstrates a full-stack AI implementation, moving beyond a simple chatbot into a grounded data pipeline:

Brain: OpenAI gpt-4o-mini

Vector Database: ChromaDB (Persistent storage for semantic search)

Embeddings: sentence-transformers/all-MiniLM-L6-v2

Framework: Streamlit for the interactive UI

Retrieval Logic: Custom semantic search with query normalization to handle user typos and context mapping.

🧠 What is RAG? (Retrieval-Augmented Generation)
Unlike standard chatbots that might "hallucinate" or give generic answers, this project uses a RAG architecture.

Ingestion: My resume (PDF), GitHub Readmes (Markdown), and personal bio are chunked and converted into mathematical vectors.

Retrieval: When you ask a question, the system searches the ChromaDB for the most relevant "chunks."

Generation: The LLM uses ONLY those specific chunks to formulate a factual, evidence-based answer.

🌟 Key Features
Multi-Source Context: Combines data from my professional resume and my actual GitHub code repositories.

Athletic Background: Integrated insights from my time as a D1 Decathlete (University of Houston), highlighting discipline and performance.

Typo-Tolerance: Custom logic to handle common search variations (e.g., "Kevins" vs "Kevin's").

Easter Egg: Includes hidden triggers for fans of the Houston Cougars or Decathlon enthusiasts.