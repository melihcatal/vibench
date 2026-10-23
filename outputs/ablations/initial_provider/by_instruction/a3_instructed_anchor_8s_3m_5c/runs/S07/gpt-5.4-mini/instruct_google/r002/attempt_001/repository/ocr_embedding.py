from google.cloud import aiplatform

from document_models import normalize_text


def embed_ocr_sections(sections, project: str, location: str, model_name: str = "textembedding-gecko@003"):
    aiplatform.init(project=project, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    texts = [normalize_text(section) for section in sections]
    return [embedding.values for embedding in model.get_embeddings(texts)]
