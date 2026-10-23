import os
import json
from google.cloud import speech
from .speech_client import SpeechClient
from .speech_models import SpeechSynthesisOutput

def generate_qa_prompt(script: str) -> str:
    """Create a simple QA prompt from a narration script.

    For the purpose of this task we extract the first sentence as a question and
    the rest as an answer. Real implementations would use more sophisticated parsing.
    """
    sentences = script.split('. ')
    if not sentences:
        return ''
    question = sentences[0] + '. '
    answer = ' '.join(sentences[1:])
    return f'Q: {question}A: {answer}'


def qa_workflow(script: str, audio_bytes: bytes) -> str:
    """Combine generation of a QA prompt and transcription of the synthesized speech.

    Returns the verified answer text.
    """
    prompt = generate_qa_prompt(script)
    # Synthesize prompt (re-use existing synthesis functions if needed) - placeholder
    # Here we just verify the transcription of the provided audio.
    verified_answer = transcribe_qa_sample(audio_bytes)
    return verified_answer
