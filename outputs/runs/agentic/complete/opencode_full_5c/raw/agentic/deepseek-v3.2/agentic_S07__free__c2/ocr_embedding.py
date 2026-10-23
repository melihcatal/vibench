import os
import numpy as np
from typing import List, Dict, Any, Optional, Union
from sklearn.metrics.pairwise import cosine_similarity


def embed_ocr_text(text: str, model: str = "embed-english-v3.0") -> List[float]:
    """
    Embed extracted document text for semantic retrieval using Cohere Embed API.

    Args:
        text: Text to embed
        model: Cohere embedding model to use

    Returns:
        Embedding vector as list of floats
    """
    import cohere

    co = cohere.Client(os.environ.get("COHERE_API_KEY", "your-api-key"))

    response = co.embed(texts=[text], model=model, input_type="search_document")

    return response.embeddings[0]


def embed_batch_ocr_texts(
    texts: List[str], model: str = "embed-english-v3.0"
) -> List[List[float]]:
    """
    Embed multiple OCR texts in batch using Cohere Embed API.

    Args:
        texts: List of texts to embed
        model: Cohere embedding model to use

    Returns:
        List of embedding vectors
    """
    import cohere

    co = cohere.Client(os.environ.get("COHERE_API_KEY", "your-api-key"))

    response = co.embed(texts=texts, model=model, input_type="search_document")

    return response.embeddings


def embed_document_sections(
    sections: Dict[str, str], model: str = "embed-english-v3.0"
) -> Dict[str, List[float]]:
    """
    Embed different sections of a document.

    Args:
        sections: Dictionary mapping section names to text
        model: Cohere embedding model to use

    Returns:
        Dictionary mapping section names to embeddings
    """
    import cohere

    co = cohere.Client(os.environ.get("COHERE_API_KEY", "your-api-key"))

    section_names = []
    section_texts = []

    for section_name, section_text in sections.items():
        if section_text.strip():
            section_names.append(section_name)
            section_texts.append(section_text)

    if not section_texts:
        return {}

    response = co.embed(texts=section_texts, model=model, input_type="search_document")

    embeddings = {}
    for i, section_name in enumerate(section_names):
        embeddings[section_name] = response.embeddings[i]

    return embeddings


def semantic_search(
    query: str, document_embeddings: Dict[str, List[float]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform semantic search over embedded document sections.

    Args:
        query: Search query
        document_embeddings: Dictionary of section embeddings
        top_k: Number of top results to return

    Returns:
        List of search results with similarity scores
    """
    import cohere

    co = cohere.Client(os.environ.get("COHERE_API_KEY", "your-api-key"))

    query_response = co.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    )

    query_embedding = np.array(query_response.embeddings[0])

    results = []

    for section_name, embedding in document_embeddings.items():
        doc_embedding = np.array(embedding)

        similarity = cosine_similarity(
            query_embedding.reshape(1, -1), doc_embedding.reshape(1, -1)
        )[0][0]

        results.append({"section": section_name, "similarity": float(similarity)})

    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_k]


def cluster_document_sections(
    embeddings: Dict[str, List[float]], n_clusters: int = 3
) -> Dict[str, int]:
    """
    Cluster document sections based on semantic similarity.

    Args:
        embeddings: Dictionary of section embeddings
        n_clusters: Number of clusters to create

    Returns:
        Dictionary mapping section names to cluster labels
    """
    from sklearn.cluster import KMeans

    if not embeddings:
        return {}

    section_names = list(embeddings.keys())
    embedding_matrix = np.array([embeddings[name] for name in section_names])

    kmeans = KMeans(n_clusters=min(n_clusters, len(section_names)), random_state=42)
    cluster_labels = kmeans.fit_predict(embedding_matrix)

    clustering = {}
    for i, section_name in enumerate(section_names):
        clustering[section_name] = int(cluster_labels[i])

    return clustering


def compute_semantic_similarity(
    text1: str, text2: str, model: str = "embed-english-v3.0"
) -> float:
    """
    Compute semantic similarity between two texts.

    Args:
        text1: First text
        text2: Second text
        model: Cohere embedding model to use

    Returns:
        Cosine similarity score between 0 and 1
    """
    import cohere

    co = cohere.Client(os.environ.get("COHERE_API_KEY", "your-api-key"))

    response = co.embed(texts=[text1, text2], model=model, input_type="search_document")

    embedding1 = np.array(response.embeddings[0])
    embedding2 = np.array(response.embeddings[1])

    similarity = cosine_similarity(
        embedding1.reshape(1, -1), embedding2.reshape(1, -1)
    )[0][0]

    return float(similarity)


def create_document_index(
    embeddings: Dict[str, List[float]], metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a search index for document embeddings.

    Args:
        embeddings: Dictionary of section embeddings
        metadata: Optional metadata for sections

    Returns:
        Search index dictionary
    """
    index = {
        "embeddings": embeddings,
        "metadata": metadata or {},
        "dimension": len(next(iter(embeddings.values()))) if embeddings else 0,
        "total_sections": len(embeddings),
    }

    return index


def find_similar_documents(
    query_embedding: List[float], document_indexes: List[Dict[str, Any]], top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Find similar documents based on embeddings.

    Args:
        query_embedding: Query embedding vector
        document_indexes: List of document indexes
        top_k: Number of top results to return

    Returns:
        List of similar documents with similarity scores
    """
    query_vec = np.array(query_embedding)

    results = []

    for doc_index in document_indexes:
        doc_embeddings = doc_index.get("embeddings", {})
        if not doc_embeddings:
            continue

        doc_embedding_matrix = np.array(list(doc_embeddings.values()))

        similarities = cosine_similarity(
            query_vec.reshape(1, -1), doc_embedding_matrix
        )[0]

        avg_similarity = float(np.mean(similarities))
        max_similarity = float(np.max(similarities))

        results.append(
            {
                "document_id": doc_index.get("metadata", {}).get("id", "unknown"),
                "avg_similarity": avg_similarity,
                "max_similarity": max_similarity,
                "total_sections": len(doc_embeddings),
                "metadata": doc_index.get("metadata", {}),
            }
        )

    results.sort(key=lambda x: x["avg_similarity"], reverse=True)

    return results[:top_k]
