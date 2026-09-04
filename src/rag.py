from dotenv import load_dotenv
load_dotenv()

import os
import json
import pickle
from pathlib import Path

import faiss
import numpy as np
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

ARTICLES_FILE = "data/support_articles.json"
VECTOR_STORE_DIR = Path("vector_store")


def load_articles():
    with open(ARTICLES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def create_embeddings():
    articles = load_articles()

    embeddings = []
    metadata = []

    for article in articles:
        text = f"{article['title']} {article['content']}"

        try:
            response = genai.embed_content(
                model="models/gemini-embedding-001",
                content=text
            )

            embeddings.append(response["embedding"])
            metadata.append(article)

        except Exception as e:
            print(f"Error embedding article {article.get('id', '?')}: {e}")
            raise

    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(
        index,
        str(VECTOR_STORE_DIR / "index.faiss")
    )

    with open(VECTOR_STORE_DIR / "metadata.pkl", "wb") as file:
        pickle.dump(metadata, file)

    print(f"FAISS index created successfully ({len(articles)} articles)")


def load_index():
    index = faiss.read_index(
        str(VECTOR_STORE_DIR / "index.faiss")
    )

    with open(VECTOR_STORE_DIR / "metadata.pkl", "rb") as file:
        metadata = pickle.load(file)

    return index, metadata


def search_articles(query, top_k=3):
    index, metadata = load_index()

    response = genai.embed_content(
        model="models/gemini-embedding-001",
        content=query
    )

    query_embedding = np.array(
        [response["embedding"]],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results


if __name__ == "__main__":
    create_embeddings()