# AI-powered-Knowledge-Base-Chat
# AI Knowledge Base Chat

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions based on their content. The application provides accurate answers with source citations and confidence scores.

##  Features

-  Upload multiple PDF documents
-  Semantic search using embeddings
-  Natural language question answering
-  Confidence scores for each answer
-  Source citation with document and page references
-  Hallucination prevention (only answers from documents)
-  Clean and intuitive user interface
- Real-time processing

##  Architecture

The application follows a RAG (Retrieval-Augmented Generation) architecture:

1. **Document Processing**: PDFs are loaded, text extracted, and split into chunks
2. **Embedding Generation**: Each chunk is converted to a vector embedding
3. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search
4. **Query Processing**: User questions are embedded and matched against stored chunks
5. **Answer Generation**: Relevant chunks are fed to LLM to generate answers
6. **Source Citation**: Retrieved chunks are displayed as sources

### Tech Stack

- **Frontend**: Streamlit
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **LLM**: OpenAI GPT-3.5 Turbo (configurable)
- **PDF Processing**: PyPDF2 + LangChain
- **Language**: Python 3.9+

##  Installation

### Prerequisites

- Python 3.9+
- OpenAI API key (if using OpenAI)
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/knowledge-base-chat.git
   cd knowledge-base-chat
