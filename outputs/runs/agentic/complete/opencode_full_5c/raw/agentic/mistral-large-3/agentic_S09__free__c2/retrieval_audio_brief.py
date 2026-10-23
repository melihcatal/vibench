from typing import List, Dict
import os
import numpy as np
from google.cloud import texttospeech
from .embed_for_search import embed_for_search
from .similarity_score import cosine_similarity


def generate_spoken_brief(query: str, documents: List[str], top_n: int = 3) -> bytes:
    """Generate a spoken brief from the top retrieved search results using Google Cloud Text-to-Speech."""
    query_embedding, doc_embeddings = embed_for_search(query, documents)

    # Rank documents by similarity to query
    similarities = [
        cosine_similarity(query_embedding, doc_embedding)
        for doc_embedding in doc_embeddings
    ]
    ranked_docs = sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, _ in ranked_docs[:top_n]]

    # Combine top documents into a brief
    brief = f"Here are the top results for your query: '{query}'. " + " ".join(top_docs)

    # Generate audio using Google Cloud Text-to-Speech
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=brief)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-D"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
