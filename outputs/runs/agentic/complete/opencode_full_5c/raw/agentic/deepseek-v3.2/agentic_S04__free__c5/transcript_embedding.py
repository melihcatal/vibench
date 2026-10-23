from google.cloud import aiplatform
from google.cloud.aiplatform import matching_engine
from google.cloud.aiplatform.matching_engine import matching_engine_index_endpoint
import numpy as np


def embed_transcript_segments(
    transcript_segments, project_id="your-project-id", location="us-central1"
):
    """Embed transcript segments for semantic retrieval using Google Vertex AI."""

    aiplatform.init(project=project_id, location=location)

    embeddings = []

    for segment in transcript_segments:
        if isinstance(segment, dict):
            text = segment.get("transcript", "")
        else:
            text = str(segment)

        if text:
            embedding = aiplatform.TextEmbedding(model="textembedding-gecko@001").embed(
                text
            )

            embedding_vector = embedding.values

            segment_embedding = {
                "text": text,
                "embedding": embedding_vector,
                "embedding_dimension": len(embedding_vector),
            }

            if isinstance(segment, dict):
                segment_embedding.update(
                    {k: v for k, v in segment.items() if k != "transcript"}
                )

            embeddings.append(segment_embedding)

    return embeddings


def create_semantic_index(
    embeddings, index_id="transcript_index", endpoint_id="transcript_endpoint"
):
    """Create a semantic search index for transcript embeddings."""

    index = matching_engine.MatchingEngineIndex.create_tree_ah_index(
        display_name=index_id,
        contents_delta_uri="gs://your-bucket/embeddings",
        dimensions=embeddings[0]["embedding_dimension"] if embeddings else 768,
        approximate_neighbors_count=150,
        leaf_node_embedding_count=1000,
        leaf_nodes_to_search_percent=50,
    )

    endpoint = matching_engine.MatchingEngineIndexEndpoint.create(
        display_name=endpoint_id,
        public_endpoint_enabled=True,
    )

    endpoint.deploy_index(index=index, deployed_index_id=f"{index_id}_deployed")

    return {
        "index": index,
        "endpoint": endpoint,
        "index_resource_name": index.resource_name,
        "endpoint_resource_name": endpoint.resource_name,
    }


def search_similar_transcripts(query_text, endpoint, top_k=5):
    """Search for similar transcripts using semantic similarity."""

    query_embedding = aiplatform.TextEmbedding(model="textembedding-gecko@001").embed(
        query_text
    )

    response = endpoint.find_neighbors(
        deployed_index_id="transcript_index_deployed",
        queries=[query_embedding.values],
        num_neighbors=top_k,
    )

    results = []
    for neighbor in response[0]:
        results.append(
            {
                "id": neighbor.id,
                "distance": neighbor.distance,
                "metadata": neighbor.metadata,
            }
        )

    return results


if __name__ == "__main__":
    segments = [
        {
            "transcript": "Discussion about quarterly financial results",
            "segment_id": "seg1",
        },
        {
            "transcript": "Marketing campaign strategy presentation",
            "segment_id": "seg2",
        },
    ]

    embeddings = embed_transcript_segments(segments)
    print(f"Created {len(embeddings)} embeddings")
