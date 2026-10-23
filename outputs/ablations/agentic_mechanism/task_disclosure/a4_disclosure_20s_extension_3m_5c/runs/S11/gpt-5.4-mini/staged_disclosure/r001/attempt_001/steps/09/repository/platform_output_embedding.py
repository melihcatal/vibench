import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_platform_outputs(outputs: List[str], model: str = DEFAULT_EMBEDDING_MODEL) -> Dict[str, Any]:
    client = _client()
    response = client.embeddings.create(model=model, input=outputs)
    return {
        "provider": "openai",
        "model": model,
        "embeddings": [item.embedding for item in response.data],
    }


def embed_platform_output(output: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    return embed_platform_outputs([output], model=model)["embeddings"][0]


def main() -> None:
    import sys

    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("no input provided")
    result = embed_platform_output(text)
    print(result)


if __name__ == "__main__":
    main()
