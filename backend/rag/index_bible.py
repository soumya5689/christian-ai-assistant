#index_bible.py

import json
from pathlib import Path
import chromadb

from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_PATH = ROOT / "data" / "processed_bible.json"

print(f"Loading Bible from {INPUT_PATH}...")

with open(
    INPUT_PATH,
    "r",
    encoding="utf-8"
) as f:

    verses = json.load(f)

print(f"Loaded {len(verses)} verses")

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Creating ChromaDB...")

CHROMA_PATH = ROOT / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="bible"
)

batch_size = 500

for i in range(0, len(verses), batch_size):

    batch = verses[i:i+batch_size]

    ids = []
    docs = []
    metadatas = []

    for verse in batch:

        verse_id = (
            f"{verse['book']}_"
            f"{verse['chapter']}_"
            f"{verse['verse']}"
        )

        ids.append(verse_id)

        docs.append(
            verse["text"]
        )

        metadatas.append(
            {
                "book": verse["book"],
                "chapter": verse["chapter"],
                "verse": verse["verse"]
            }
        )

    embeddings = model.encode(
        docs
    ).tolist()

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Indexed {i+len(batch)} verses"
    )

print("Bible indexing complete")