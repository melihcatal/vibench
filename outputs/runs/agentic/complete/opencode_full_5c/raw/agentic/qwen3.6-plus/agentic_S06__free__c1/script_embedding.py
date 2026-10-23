from __future__ import annotations

from speech_client import create_openai_client, OPENAI_EMBEDDING_MODEL
from speech_models import EmbeddingRequest, EmbeddingResponse, normalize_text


def embed_script(
    text: str,
    model: str | None = None,
    api_key: str | None = None,
) -> EmbeddingResponse:
    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("Input text is empty")

    selected_model = model or OPENAI_EMBEDDING_MODEL

    client = create_openai_client(api_key=api_key)

    response = client.embeddings.create(
        model=selected_model,
        input=normalized,
    )

    embedding = response.data[0].embedding

    return EmbeddingResponse(
        embedding=embedding,
        model=selected_model,
        text=normalized,
    )


def embed_scripts_batch(
    texts: list[str],
    model: str | None = None,
    api_key: str | None = None,
) -> list[EmbeddingResponse]:
    selected_model = model or OPENAI_EMBEDDING_MODEL
    client = create_openai_client(api_key=api_key)

    normalized_texts = [normalize_text(t) for t in texts if normalize_text(t)]

    if not normalized_texts:
        raise ValueError("All input texts are empty")

    response = client.embeddings.create(
        model=selected_model,
        input=normalized_texts,
    )

    results = []
    for idx, data in enumerate(response.data):
        results.append(
            EmbeddingResponse(
                embedding=data.embedding,
                model=selected_model,
                text=normalized_texts[idx],
            )
        )

    return results
