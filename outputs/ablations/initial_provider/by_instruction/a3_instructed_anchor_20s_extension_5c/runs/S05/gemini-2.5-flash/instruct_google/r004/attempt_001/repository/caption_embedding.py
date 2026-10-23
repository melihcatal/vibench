import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your project ID and region
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    embeddings = []
    for chunk in caption_chunks:
        # The embed method can take a list of texts, but for chunk by chunk processing,
        # we can embed each chunk individually or batch them if desired for performance.
        response = model.embed_text(text=chunk)
        embeddings.append(response.embeddings[0].values)

    return embeddings
