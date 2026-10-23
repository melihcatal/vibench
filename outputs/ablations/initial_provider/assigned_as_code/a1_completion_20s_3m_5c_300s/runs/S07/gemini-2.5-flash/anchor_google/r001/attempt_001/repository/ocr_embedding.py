import vertexai
from vertexai.language_models import TextEmbeddingModel

def ocr_embedding(text_sections: list[str], project_id: str, location: str):
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    
    embeddings = []
    for section in text_sections:
        # The TextEmbeddingModel expects a list of texts to embed.
        # We'll embed each section individually for simplicity here.
        # For larger inputs, batching might be more efficient.
        response = model.get_embeddings([section])
        embeddings.append(response[0].values)

    return {"embeddings": embeddings}
