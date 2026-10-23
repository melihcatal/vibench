import os
from openai import OpenAI
from speech_models import Transcript
from typing import List


def get_transcript_embeddings(transcript: Transcript) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=api_key)
    texts = [segment.text for segment in transcript.segments]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [data.embedding for data in response.data]
