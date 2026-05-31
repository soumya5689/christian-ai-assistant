from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent.parent

CHROMA_PATH = ROOT / "chroma_db"

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    "bible"
)

print(
    f"Collection Count: {collection.count()}"
)


def search_bible(
    query: str,
    top_k: int = 5
):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    results = search_bible(
        "forgiveness"
    )

    print(
        results["metadatas"][0]
    )