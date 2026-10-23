import os
from google.cloud import aiplatform
from google.cloud.aiplatform import matching_engine
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import (
    Namespace,
)


def embed_transcript_segments(segments, project_id=None, location="us-central1"):
    """Embed transcript segments for semantic retrieval using Google Vertex AI."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

    aiplatform.init(project=project_id, location=location)

    embeddings = []

    for i, segment in enumerate(segments):
        if isinstance(segment, dict):
            segment_text = segment.get("transcript", "")
        else:
            segment_text = (
                segment.transcript if hasattr(segment, "transcript") else str(segment)
            )

        if segment_text:
            embedding = aiplatform.TextEmbedding(model="textembedding-gecko@003").embed(
                [segment_text]
            )[0]

            embedding_data = {
                "id": f"segment_{i}",
                "embedding": embedding.values,
                "text": segment_text,
                "dimensions": len(embedding.values),
            }

            if isinstance(segment, dict):
                embedding_data.update(
                    {
                        "start_time": segment.get("start_time"),
                        "end_time": segment.get("end_time"),
                        "speaker_tag": segment.get("speaker_tag"),
                    }
                )

            embeddings.append(embedding_data)

    return embeddings
