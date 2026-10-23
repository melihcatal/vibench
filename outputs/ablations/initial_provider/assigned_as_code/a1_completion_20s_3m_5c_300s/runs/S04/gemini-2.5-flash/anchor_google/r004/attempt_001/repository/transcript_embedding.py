from google.cloud import aiplatform

def embed_transcript_segments(text_segments, project_id, location="us-central1"):
    aiplatform.init(project=project_id, location=location)

    # Using the text-embedding-004 model for text embeddings
    # https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.predict(text_segments)

    return [embedding.values for embedding in embeddings]
