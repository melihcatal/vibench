from google.cloud import aiplatform
from google.cloud.aiplatform import Model
from typing import List, Dict, Any


def embed_caption_chunks(
    transcript_chunks: List[Dict[str, Any]],
    project_id: str = "your-google-cloud-project",
    location: str = "us-central1",
) -> List[Dict[str, Any]]:
    """Embeds caption chunks for semantic meeting search using Google Cloud Vertex AI."""
    aiplatform.init(project=project_id, location=location)

    model = Model(
        "projects/{}/locations/{}/models/textembedding-gecko@latest".format(
            project_id, location
        )
    )
    endpoint = model.deployed_models[0].resource_name

    texts = [
        chunk["text"]
        for chunk in transcript_chunks
        if chunk["is_final"] and chunk["text"].strip()
    ]

    if not texts:
        return []

    response = model.predict(instances=[{"content": text} for text in texts])

    embeddings = response.predictions

    return [
        {
            "text": texts[i],
            "embedding": embedding,
            "start_time": transcript_chunks[i].get("start_time", 0.0),
            "end_time": transcript_chunks[i].get("end_time", 0.0),
        }
        for i, embedding in enumerate(embeddings)
    ]
