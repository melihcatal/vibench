import os
from openai import OpenAI
from typing import List
from speech_models import TranscriptionResponse

def get_transcript_embeddings(transcript: TranscriptionResponse) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not transcript.text:
        raise ValueError("No text to embed.")
    
    response = client.embeddings.create(
        input=transcript.text,
        model="text-embedding-ada-002"
    )
    
    return response.data[0].embedding