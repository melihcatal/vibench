import os
import json
from typing import List, Dict, Any, Optional, Union
import cohere
import numpy as np
from datetime import datetime


def embed_audit_notes(
    notes: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        response = co.embed(texts=notes, model=model, input_type="search_document")

        return response.embeddings
    except Exception as e:
        raise RuntimeError(f"Cohere embedding failed: {e}")


def embed_crypto_audit_entry(
    audit_entry: Dict[str, Any], model: str = "embed-english-v3.0"
) -> Dict[str, Any]:
    note_text = audit_entry.get("note", "")
    operation = audit_entry.get("operation", "")
    key_id = audit_entry.get("key_id", "")
    timestamp = audit_entry.get("timestamp", "")

    embedding_text = f"""
    Operation: {operation}
    Key ID: {key_id}
    Timestamp: {timestamp}
    Note: {note_text}
    """

    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[embedding_text], model=model, input_type="search_document"
        )

        result = audit_entry.copy()
        result["embedding"] = response.embeddings[0]
        result["embedding_model"] = model
        result["embedding_timestamp"] = datetime.now().isoformat()

        return result
    except Exception as e:
        raise RuntimeError(f"Cohere embedding failed: {e}")


def search_similar_audit_notes(
    query: str,
    embedded_notes: List[Dict[str, Any]],
    model: str = "embed-english-v3.0",
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        query_response = co.embed(texts=[query], model=model, input_type="search_query")

        query_embedding = np.array(query_response.embeddings[0])

        similarities = []
        for note in embedded_notes:
            if "embedding" in note:
                note_embedding = np.array(note["embedding"])
                similarity = np.dot(query_embedding, note_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(note_embedding)
                )
                similarities.append((similarity, note))

        similarities.sort(key=lambda x: x[0], reverse=True)

        results = []
        for similarity, note in similarities[:top_k]:
            result = note.copy()
            result["similarity_score"] = float(similarity)
            results.append(result)

        return results
    except Exception as e:
        raise RuntimeError(f"Cohere search failed: {e}")


def create_audit_note_clusters(
    audit_notes: List[Dict[str, Any]],
    model: str = "embed-english-v3.0",
    num_clusters: int = 5,
) -> Dict[str, Any]:
    note_texts = []
    for note in audit_notes:
        note_text = note.get("note", "")
        operation = note.get("operation", "")
        text = f"{operation}: {note_text}"
        note_texts.append(text)

    if len(note_texts) < num_clusters:
        num_clusters = len(note_texts)

    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        embeddings = co.embed(
            texts=note_texts, model=model, input_type="clustering"
        ).embeddings

        from sklearn.cluster import KMeans

        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)

        clusters = {}
        for i, (note, label) in enumerate(zip(audit_notes, cluster_labels)):
            cluster_key = f"cluster_{label}"
            if cluster_key not in clusters:
                clusters[cluster_key] = {
                    "cluster_id": label,
                    "notes": [],
                    "size": 0,
                    "representative_notes": [],
                }

            note_with_cluster = note.copy()
            note_with_cluster["cluster_id"] = label
            clusters[cluster_key]["notes"].append(note_with_cluster)
            clusters[cluster_key]["size"] += 1

        for cluster_key in clusters:
            cluster_notes = clusters[cluster_key]["notes"]
            if cluster_notes:
                clusters[cluster_key]["representative_notes"] = cluster_notes[:3]

        return {
            "total_notes": len(audit_notes),
            "num_clusters": num_clusters,
            "clusters": clusters,
        }
    except Exception as e:
        raise RuntimeError(f"Clustering failed: {e}")


def generate_audit_summary_embedding(
    audit_summary: str, model: str = "embed-english-v3.0"
) -> Dict[str, Any]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[audit_summary], model=model, input_type="search_document"
        )

        return {
            "summary": audit_summary,
            "embedding": response.embeddings[0],
            "model": model,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise RuntimeError(f"Cohere embedding failed: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        try:
            with open(input_file, "r") as f:
                audit_notes = json.load(f)

            if isinstance(audit_notes, list):
                embedded = []
                for note in audit_notes[:5]:
                    embedded_note = embed_crypto_audit_entry(note)
                    embedded.append(embedded_note)

                print(f"Embedded {len(embedded)} audit notes")
                print(json.dumps(embedded[:2], indent=2))
            else:
                print("Input must be a list of audit notes", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
