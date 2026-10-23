import os
import google.generativeai as genai
from speech_models import TranscriptSegment
from typing import List

def summarize_transcription_results(segments: List[TranscriptSegment]) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    full_transcript = " ".join([s.text for s in segments])

    prompt = f"Please summarize the following transcript:

{full_transcript}

Summary:"

    response = model.generate_content(prompt)
    return response.text
