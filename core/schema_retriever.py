import chromadb
from sentence_transformers import SentenceTransformer


class SchemaRetriever:
    def __init__(self):
        self.embedding_model = SentenceTransformer("BAAI/bge-small-en")

        self.client = chromadb.PersistentClient(path="chroma_store")

        self.collection = self.client.get_or_create_collection(
            name="schema_index"
        )

    def retrieve(self, question, top_k=2):
        embedding = self.embedding_model.encode(question).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

        return results["documents"][0]


if __name__ == "__main__":
    retriever = SchemaRetriever()

    query = "top customers by revenue"

    schema = retriever.retrieve(query)

    print("\nRetrieved schema context:\n")

    for item in schema:
        print("-", item)