# AI-powered-Knowledge-Base-Chat


# 📚 AI-Powered Knowledge Base Chat

A **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions based on their content. Built with **Streamlit**, **OpenAI**, **ChromaDB**, and **Sentence Transformers**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📤 **PDF Upload** | Upload one or multiple PDF documents |
| 🔍 **Semantic Search** | Find relevant content using embeddings |
| 💬 **Natural Language Q&A** | Ask questions in plain English |
| 📊 **Confidence Scores** | Each answer comes with a confidence level |
| 📚 **Source Citation** | Shows document name and page number |
| 🚫 **Hallucination Prevention** | Responds "I don't know" when unsure |
| 🎯 **Clean UI** | Intuitive and user-friendly interface |


---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB |
| LLM | OpenAI GPT-3.5 Turbo |
| PDF Processing | PyPDF |
| Language | Python 3.9+ |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/poojahiwale1908-creator/Al-powered-Knowledge-Base-Chat.git
cd Al-powered-Knowledge-Base-Chat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key

# Run the application
streamlit run app.py


📖 Usage Guide
1️⃣ Upload Documents
Click "Browse files" in the sidebar

Select one or more PDF files

Click "Process Documents"

2️⃣ Ask Questions
Type your question in the chat input

Press Enter or click Send

View the answer with confidence score and sources

3️⃣ Manage Chat
Use "Clear Chat" to reset conversation

Use "Clear Documents" to remove all documents
