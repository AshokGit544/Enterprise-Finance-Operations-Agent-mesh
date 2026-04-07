from sentence_transformers import SentenceTransformer
from app.data.policy_documents import get_policy_documents
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def search_relevant_policy(query: str):
    policies = get_policy_documents()

    searchable_texts = [
        f"{p['title']} {p['category']} {p['keywords']} {p['text']}"
        for p in policies
    ]

    policy_embeddings = model.encode(searchable_texts, convert_to_numpy=True)
    query_embedding = model.encode([query], convert_to_numpy=True)[0]

    scores = np.dot(policy_embeddings, query_embedding) / (
        np.linalg.norm(policy_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    best_index = int(np.argmax(scores))
    return policies[best_index]