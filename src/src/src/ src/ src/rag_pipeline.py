import os
import openai
from src.document_processor import DocumentProcessor
from src.embedding import EmbeddingGenerator
from src.vector_store import VectorStore

class RAGPipeline:
    def __init__(self):
        self.processor = DocumentProcessor()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
        openai.api_key = os.getenv("OPENAI_API_KEY", "")

    def add_documents(self, files):
        all_chunks = []
        for file in files:
            chunks, _ = self.processor.process_document(file)
            all_chunks.extend(chunks)

        if not all_chunks:
            return {"processed": 0, "chunks": 0}

        texts = [c['content'] for c in all_chunks]
        embeddings = self.embedding_gen.generate_embeddings(texts)
        self.vector_store.add_documents(all_chunks, embeddings)
        return {"processed": len(files), "chunks": len(all_chunks)}

    def query(self, question):
        if not question or not question.strip():
            return {"answer": "Please ask a valid question.", "sources": [], "confidence": 0.0}

        if self.vector_store.get_count() == 0:
            return {"answer": "Please upload documents first.", "sources": [], "confidence": 0.0}

        query_emb = self.embedding_gen.generate_embedding(question)
        results = self.vector_store.search(query_emb)

        if not results:
            return {"answer": "I don't know based on the provided documents.", "sources": [], "confidence": 0.0}

        # Check relevance
        if results[0]['similarity'] < 0.3:
            return {
                "answer": "I don't know based on the provided documents.",
                "sources": [{"document": r['metadata'].get('source',''), "page": r['metadata'].get('page',''), "similarity": r['similarity']} for r in results[:2]],
                "confidence": results[0]['similarity']
            }

        # Build context
        context = "\\n\\n".join([f"[{r['metadata'].get('source','')}, Page {r['metadata'].get('page','')}]\\n{r['content']}" for r in results[:3]])

        # Generate answer
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Answer based ONLY on context. If not found, say 'I don't know based on the provided documents.'"},
                    {"role": "user", "content": f"Context:\\n{context}\\n\\nQuestion: {question}"}
                ],
                temperature=0.0,
                max_tokens=300
            )
            answer = response.choices[0].message.content.strip()
        except:
            answer = "I don't know based on the provided documents."

        # Check for uncertainty
        if "don't know" in answer.lower():
            return {"answer": answer, "sources": [], "confidence": 0.0}

        return {
            "answer": answer,
            "sources": [{"document": r['metadata'].get('source',''), "page": r['metadata'].get('page',''), "similarity": r['similarity']} for r in results[:3]],
            "confidence": min(1.0, results[0]['similarity'] * 1.1)
        }

    def get_stats(self):
        return {"chunks": self.vector_store.get_count()}

    def clear_documents(self):
        self.vector_store.clear_all()
