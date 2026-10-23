import os

import openai

MODEL_ID = "text-embedding-3-small"


def embed_reasons(reasons: list[str]) -> list[list[float]]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Set it to your OpenAI API key."
        )

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=MODEL_ID,
        input=reasons,
    )

    embeddings = []
    sorted_data = sorted(response.data, key=lambda d: d.index)
    for item in sorted_data:
        embeddings.append(item.embedding)

    return embeddings
