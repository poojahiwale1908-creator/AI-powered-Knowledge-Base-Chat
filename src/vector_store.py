import uuid
import chromadb

class VectorStore:
    def __init__(self, persist_dir="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = None
        self.create_collection()

    def create_collection(self, name="documents"):
        try:
            self.client.delete_collection(name)
        except:
            pass
        self.collection = self.client.create_collection(name=name)

    def add_documents(self, chunks, embeddings):
        if not chunks or not embeddings:
            return

        ids = [str(uuid.uuid4()) for _ in chunks]
        docs = [c['content'] for c in chunks]
        metas = [{"source": c.get("source", "unknown"), "page": c.get("page", "unknown")} for c in chunks]

        self.collection.add(embeddings=embeddings, documents=docs, metadatas=metas, ids=ids)

    def search(self, embedding, top_k=5):
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)

        formatted = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'similarity': 1.0 - results['distances'][0][i] if results['distances'] else 0.0
                })
        return formatted

    def get_count(self):
        return self.collection.count() if self.collection else 0

    def clear_all(self):
        if self.collection:
            self.collection.delete(ids=self.collection.get()['ids'])
