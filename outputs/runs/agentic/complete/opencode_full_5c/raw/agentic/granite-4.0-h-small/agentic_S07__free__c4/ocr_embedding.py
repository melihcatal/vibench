import openai
from document_client import DocumentClient
from document_models import EmbeddingRequest, EmbeddingResponse

def embed_sections(sections: list[str], model: str = "text-embedding-ada-002") -> EmbeddingResponse:
    """Generate embeddings for each document section using OpenAI's embedding API.",
    client = DocumentClient(service="azure_ocr")  # any service works; we just use the model name
    embeddings = []
    for sec in sections:
        resp = openai.Embedding.create(
            model=model,
            input=sec
        )
        embeddings.append(resp['data'][0]['embedding'])
    return EmbeddingResponse(embeddings=embeddings)


def embed_document_text(image_path: str, chunk_size: int = 500) -> EmbeddingResponse:
    """Extract text via OCR, split into chunks, and embed each chunk.",
    client = DocumentClient(service="azure_ocr")
    with open(image_path, "rb") as img:
        ocr_result = client.ocr_image(image_bytes=img.read())
        ocr_text = ocr_result.get("text", "")
    chunks = [ocr_text[i:i+chunk_size] for i in range(0, len(ocr_text), chunk_size)]
    return embed_sections(chunks)
