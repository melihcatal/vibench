import os
import sys
import json

import dashscope
from dashscope import TextEmbedding

from observability_models import IncidentFinding


DASHSCOPE_EMBEDDING_MODEL = "text-embedding-v3"


def embed_log_message(text: str, dimensions: int = 1024) -> dict:
    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "")

    try:
        response = TextEmbedding.call(
            model=DASHSCOPE_EMBEDDING_MODEL,
            input=text,
            dimension=dimensions,
        )

        result = {
            "text": text,
            "model": DASHSCOPE_EMBEDDING_MODEL,
            "embedding": [],
            "dimensions": dimensions,
        }

        if response.status_code == 200:
            if response.output and response.output.embeddings:
                embedding_data = response.output.embeddings[0]
                result["embedding"] = embedding_data.embedding
                result["dimensions"] = len(embedding_data.embedding)
        else:
            result["error"] = (
                f"Embedding API returned: {response.code} - {response.message}"
            )

        return result
    except Exception as e:
        return {
            "text": text,
            "model": DASHSCOPE_EMBEDDING_MODEL,
            "embedding": [],
            "dimensions": dimensions,
            "error": str(e),
        }


def embed_multiple_log_messages(texts: list[str], dimensions: int = 1024) -> list[dict]:
    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "")

    try:
        response = TextEmbedding.call(
            model=DASHSCOPE_EMBEDDING_MODEL,
            input=texts,
            dimension=dimensions,
        )

        results = []
        if response.status_code == 200:
            if response.output and response.output.embeddings:
                for emb in response.output.embeddings:
                    results.append(
                        {
                            "text": texts[emb.text_index]
                            if hasattr(emb, "text_index")
                            and emb.text_index < len(texts)
                            else "",
                            "model": DASHSCOPE_EMBEDDING_MODEL,
                            "embedding": emb.embedding,
                            "dimensions": len(emb.embedding),
                        }
                    )
        else:
            for text in texts:
                results.append(
                    {
                        "text": text,
                        "model": DASHSCOPE_EMBEDDING_MODEL,
                        "embedding": [],
                        "dimensions": dimensions,
                        "error": f"API error: {response.code} - {response.message}",
                    }
                )

        return results
    except Exception as e:
        return [
            {
                "text": text,
                "model": DASHSCOPE_EMBEDDING_MODEL,
                "embedding": [],
                "dimensions": dimensions,
                "error": str(e),
            }
            for text in texts
        ]


def annotate_findings_with_embeddings(
    findings: list[IncidentFinding],
    dimensions: int = 1024,
) -> list[IncidentFinding]:
    messages = [
        f.log_entry.get("message", "") for f in findings if f.log_entry.get("message")
    ]

    if not messages:
        return findings

    embedding_results = embed_multiple_log_messages(messages, dimensions=dimensions)

    annotated = []
    emb_idx = 0
    for finding in findings:
        message = finding.log_entry.get("message", "")
        if message and emb_idx < len(embedding_results):
            finding.embedding = embedding_results[emb_idx].get("embedding", [])
            emb_idx += 1
        annotated.append(finding)
    return annotated


def compute_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
    if not embedding_a or not embedding_b:
        return 0.0

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Sample log message to embed"
    result = embed_log_message(text)
    output = {k: v for k, v in result.items() if k != "embedding"}
    output["embedding_preview"] = (
        result.get("embedding", [])[:5] if result.get("embedding") else []
    )
    print(json.dumps(output, indent=2))
