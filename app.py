import os
import streamlit as st
from src.rag_pipeline import RAGPipeline

# Set page config
st.set_page_config(
    page_title="AI Knowledge Base Chat",
    page_icon="📚",
    layout="wide"
)

# Initialize pipeline
@st.cache_resource
def get_pipeline():
    return RAGPipeline()

pipeline = get_pipeline()

# Title
st.title("📚 AI Knowledge Base Chat")
st.markdown("Upload PDF documents and ask questions about their content")

# Sidebar
with st.sidebar:
    st.header("📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("📥 Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                # Create file objects (same as Colab)
                class FileObj:
                    def __init__(self, name, content):
                        self.name = name
                        self.content = content
                        self.size = len(content)
                    def getvalue(self):
                        return self.content
                
                file_objects = [FileObj(f.name, f.getvalue()) for f in uploaded_files]
                stats = pipeline.add_documents(file_objects)
                st.success(f"✅ Processed {stats['processed']} files, {stats['chunks']} chunks")
    
    st.divider()
    st.header("📊 Statistics")
    stats = pipeline.get_stats()
    st.metric("Document Chunks", stats.get('chunks', 0))
    
    if st.button("🗑️ Clear Documents", use_container_width=True):
        pipeline.clear_documents()
        st.rerun()

# Chat interface
st.header("💬 Ask Questions")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = pipeline.query(prompt)
            st.markdown(response['answer'])
            
            # Show confidence
            if response['confidence'] > 0:
                from src.utils import get_confidence_color
                color = get_confidence_color(response['confidence'])
                st.caption(f"Confidence: {response['confidence']:.1%}")
            
            # Show sources
            if response.get('sources'):
                with st.expander("📚 Sources"):
                    for s in response['sources']:
                        st.markdown(f"- **{s['document']}** (Page {s['page']}) - Similarity: {s['similarity']:.1%}")
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response['answer']})

  
