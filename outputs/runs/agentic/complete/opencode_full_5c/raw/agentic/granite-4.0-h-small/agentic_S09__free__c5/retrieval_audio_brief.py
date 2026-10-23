# Generate a spoken brief from retrieved search results

import json
from pathlib import Path


def retrieval_audio_brief(results_path: Path, max_sentences: int = 3) -> str:
    """Create a concise spoken brief from semantic search results.

    The results file is expected to be JSON lines where each line contains:
    {
        "id": "unique_identifier",
        "text": "...retrieved document text...",
        "score": 0.95
    }

    The brief is a concatenation of the top `max_sentences` sentences from the highest‑scoring documents.
    Returns the brief as plain text.
    """
    lines = results_path.read_text().splitlines()
    # Parse JSON lines
    parsed = [json.loads(line) for line in lines]
    # Sort by score descending
    parsed.sort(key=lambda x: x.get("score", 0), reverse=True)
    # Take top documents
    top_docs = parsed[:5]  # get a few top hits
    sentences = []
    for doc in top_docs:
        txt = doc.get("text", "")
        # Simple sentence splitting
        for sent in txt.split(". "):
            if sent:
                sentences.append(sent.strip())
                if len(sentences) >= max_sentences:
                    break
        if len(sentences) >= max_sentences:
            break
    # Join into a spoken‑ready string
    brief = " ".join(sentences)
    return brief
