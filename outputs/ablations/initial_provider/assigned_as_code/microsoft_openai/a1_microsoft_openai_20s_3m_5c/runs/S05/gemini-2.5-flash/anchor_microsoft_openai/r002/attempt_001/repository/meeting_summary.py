import os
import google.generativeai as genai

def summarize_meeting(transcript_chunks: list[str], model_name: str = "gemini-pro") -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set for Google Generative AI.")
    
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    full_transcript = "\n".join(transcript_chunks)

    prompt = f"""Summarize the following meeting transcript:

    {full_transcript}

    Summary:"""

    response = model.generate_content(prompt)
    return response.text
