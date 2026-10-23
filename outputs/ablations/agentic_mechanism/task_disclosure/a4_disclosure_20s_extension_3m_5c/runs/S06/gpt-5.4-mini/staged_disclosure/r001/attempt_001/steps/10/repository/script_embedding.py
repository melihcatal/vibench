import os
import sys
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from openai import OpenAI


@dataclass(frozen=True)
class EmbeddingConfig:
    api_key: str
    model: str = "text-embedding-3-large"


def load_embedding_config() -> EmbeddingConfig:
    return EmbeddingConfig(
        api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
    )


def create_client(api_key: str | None = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ["OPENAI_API_KEY"])


def chunk_script(text: str, max_chars: int = 8000) -> List[str]:
    parts: List[str] = []
    current: List[str] = []
    current_len = 0
    for line in text.splitlines():
        line_len = len(line) + 1
        if current and current_len + line_len > max_chars:
            parts.append("\n".join(current).strip())
            current = []
            current_len = 0
        current.append(line)
        current_len += line_len
    if current:
        parts.append("\n".join(current).strip())
    return [part for part in parts if part]


def embed_scripts(scripts: Sequence[str], model: str | None = None) -> List[List[float]]:
    config = load_embedding_config()
    client = create_client(config.api_key)
    response = client.embeddings.create(
        model=model or config.model,
        input=list(scripts),
    )
    return [item.embedding for item in response.data]


def embed_script(text: str, model: str | None = None) -> List[float]:
    chunks = chunk_script(text)
    if not chunks:
        return []
    vectors = embed_scripts(chunks, model=model)
    if len(vectors) == 1:
        return vectors[0]
    dimension = len(vectors[0])
    averaged = [0.0] * dimension
    for vector in vectors:
        for idx, value in enumerate(vector):
            averaged[idx] += value
    return [value / len(vectors) for value in averaged]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: script_embedding.py <input_file>")
    input_path = sys.argv[1]
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    embedding = embed_script(text)
    sys.stdout.write("\n".join(str(value) for value in embedding))


if __name__ == "__main__":
    main()
