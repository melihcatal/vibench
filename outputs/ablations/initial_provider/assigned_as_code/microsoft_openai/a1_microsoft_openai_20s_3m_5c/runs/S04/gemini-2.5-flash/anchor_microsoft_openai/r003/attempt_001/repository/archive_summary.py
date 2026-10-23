import os
import google.generativeai as genai
from typing import List, Dict, Any
from speech_models import TranscriptSegment

def archive_summary(segments: List[TranscriptSegment], model_name: str = "models/gemini-pro") -> Dict[str, Any]:
    # Configure the generative AI model
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel(model_name)

    full_transcript = " ".join([s.text for s in segments])

    prompt = f"Summarize the following meeting transcript:

{full_transcript}

Provide a concise summary of the key discussion points and any decisions made."

    response = model.generate_content(prompt)
    
    return {"summary": response.text}
