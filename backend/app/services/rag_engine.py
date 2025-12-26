from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from typing import List

COLLECTION_NAME = "legal_knowledge"
VECTOR_SIZE = 384
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    def retrieve(self, query: str, top_k: int = 3) -> List[dict]:
        query_vec = self.model.encode(query).tolist()
        search_result = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vec,
            limit=top_k
        )
        return [point.payload for point in search_result]
