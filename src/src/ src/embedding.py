from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
        except:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embeddings(self, texts):
        if not texts:
            return []
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def generate_embedding(self, text):
        return self.generate_embeddings([text])[0]
