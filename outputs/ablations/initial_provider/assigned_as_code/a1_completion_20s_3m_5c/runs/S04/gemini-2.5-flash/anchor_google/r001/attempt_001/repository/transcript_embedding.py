import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def transcript_embedding(text_segments: list[str], project_id: str, location: str = "us-central1"):
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = []
    for segment in text_segments:
        response = model.embed_text(text=segment)
        embeddings.append(response.embeddings[0].values)

    return embeddings
