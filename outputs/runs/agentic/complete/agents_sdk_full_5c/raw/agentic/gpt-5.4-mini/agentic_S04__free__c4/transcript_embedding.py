from __future__ import annotations

from typing import Dict, List

from speech_client import OPENAI_EMBED_MODEL, SpeechClientFactory


def transcript_embedding(segments: List[Dict[str, str]]) -> Dict[str, object]:
    client = SpeechClientFactory.create()
    text = "\n".join(segment.get("text", "") for segment in segments)
    response = client.embeddings.create(model=OPENAI_EMBED_MODEL, input=text)
    item = response.data[0]
    return {"model": OPENAI_EMBED_MODEL, "embedding": item.embedding, "index": item.index}
