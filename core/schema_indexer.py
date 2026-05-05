import chromadb
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, inspect


class SchemaIndexer:
    def __init__(self, db_path="sqlite:///data/sample.db"):
        self.engine = create_engine(db_path)
        self.inspector = inspect(self.engine)

        self.embedding_model = SentenceTransformer(
            "BAAI/bge-small-en"
        )

        self.client = chromadb.PersistentClient(path="chroma_store")

        self.collection = self.client.get_or_create_collection(
            name="schema_index"
        )

    def extract_schema(self):
        schema_docs = []

        tables = self.inspector.get_table_names()

        for table in tables:
            columns = self.inspector.get_columns(table)

            column_names = [col["name"] for col in columns]

            schema_text = f"Table {table} has columns: {', '.join(column_names)}"

            schema_docs.append((table, schema_text))

        return schema_docs

    def index_schema(self):
        schema_docs = self.extract_schema()

        for idx, (table, doc) in enumerate(schema_docs):
            embedding = self.embedding_model.encode(doc).tolist()

            self.collection.add(
                ids=[str(idx)],
                embeddings=[embedding],
                documents=[doc],
                metadatas=[{"table": table}],
            )

        print("✅ Schema indexed successfully!")

    def query_schema(self, question, top_k=3):
        embedding = self.embedding_model.encode(question).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        return results["documents"][0]


if __name__ == "__main__":
    indexer = SchemaIndexer()
    indexer.index_schema()

    test_query = "top customers by revenue"

    matches = indexer.query_schema(test_query)

    print("\nRelevant schema:")
    for match in matches:
        print("-", match)