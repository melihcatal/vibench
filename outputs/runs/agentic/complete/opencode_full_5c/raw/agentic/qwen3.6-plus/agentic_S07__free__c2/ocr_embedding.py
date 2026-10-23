import os
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> list:
    client = get_openai_client()
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def embed_document_sections(
    sections: list, model: str = OPENAI_EMBEDDING_MODEL
) -> list:
    client = get_openai_client()
    response = client.embeddings.create(input=sections, model=model)
    return [item.embedding for item in response.data]


def embed_ocr_lines(ocr_lines: list, model: str = OPENAI_EMBEDDING_MODEL) -> list:
    texts = [line.text if hasattr(line, "text") else line for line in ocr_lines]
    return embed_document_sections(texts, model)


def embed_ocr_pages(ocr_result, model: str = OPENAI_EMBEDDING_MODEL) -> list:
    page_texts = [page.text for page in ocr_result.pages]
    return embed_document_sections(page_texts, model)


def compute_similarity(embedding_a: list, embedding_b: list) -> float:
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def find_most_similar_section(
    query_text: str, sections: list, model: str = OPENAI_EMBEDDING_MODEL
) -> dict:
    query_embedding = embed_text(query_text, model)
    section_embeddings = embed_document_sections(sections, model)

    best_idx = 0
    best_score = -1.0
    for idx, sec_emb in enumerate(section_embeddings):
        score = compute_similarity(query_embedding, sec_emb)
        if score > best_score:
            best_score = score
            best_idx = idx

    return {"index": best_idx, "text": sections[best_idx], "similarity": best_score}
