import os
from typing import List, Dict, Any
from cohere import Client
from speech_models import DiarizedUtterance


def transcript_embedding(utterances: List[DiarizedUtterance]) -> List[Dict[str, Any]]:
    """
    Embeds transcript segments for semantic retrieval using Cohere's Embed API.
    """
    client = Client(api_key=os.getenv("COHERE_API_KEY"))
    texts = [
        f"Speaker {utterance.speaker}: {utterance.text}" for utterance in utterances
    ]

    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document",
    )

    return [
        {
            "speaker": utterance.speaker,
            "text": utterance.text,
            "start": utterance.start,
            "end": utterance.end,
            "embedding": embedding,
        }
        for utterance, embedding in zip(utterances, response.embeddings)
    ]
