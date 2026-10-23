from typing import Any, Dict, List

from openai import OpenAI

from speech_client import load_speech_config


MODEL = "text-embedding-3-small"


def transcript_embedding(segments: List[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=load_speech_config().api_key or None)
    response = client.embeddings.create(model=MODEL, input=segments)
    vectors = [item.embedding for item in response.data]
    return {"model": MODEL, "embeddings": vectors}
