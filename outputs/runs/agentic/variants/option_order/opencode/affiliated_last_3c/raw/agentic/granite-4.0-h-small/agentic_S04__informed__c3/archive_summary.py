import os
import json
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import NormalizedTranscript
from google.cloud import genai

# Load credentials from environment (Google Gemini / Vertex AI)
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GENAI_API_KEY)


def summarize_transcript(segments: NormalizedTranscript) -> str:
    """Generates a concise summary of a transcription using Gemini LLM.
    Returns a single summary string.
    """
    # Join all cleaned text (assuming already moderated/cleaned)
    full_text = " ".join([seg["text"] for seg in segments])
    # Gemini chat model (preview) for summarization
    model = genai.ChatModel("gemini-1.5-flash")
    response = model.predict(full_text, generation_config={"temperature": 0.2})
    return response.text.strip()
