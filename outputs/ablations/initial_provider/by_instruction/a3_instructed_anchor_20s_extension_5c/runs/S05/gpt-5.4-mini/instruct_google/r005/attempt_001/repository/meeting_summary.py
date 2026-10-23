import os

from google.cloud import generativelanguage_v1beta as gl


def summarize_meeting(chunks):
    client = gl.GenerativeServiceClient()
    model = os.getenv("GOOGLE_GENERATIVE_MODEL", "models/gemini-1.5-pro")
    text = "\n".join(chunks)
    response = client.generate_content(
        request={
            "model": model,
            "contents": [{"parts": [{"text": f"Summarize this meeting transcript:\n{text}"}]}],
        }
    )
    return response.candidates[0].content.parts[0].text if response.candidates else ""
