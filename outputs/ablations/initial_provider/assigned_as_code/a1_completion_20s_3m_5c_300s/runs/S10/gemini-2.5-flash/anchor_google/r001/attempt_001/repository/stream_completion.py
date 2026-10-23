import os

from google import genai

def stream_completion(payload, config=None):
    config = config or {}
    prompt = payload["text"]
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response_stream = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, stream=True)
        
        full_response_content = ""
        for chunk in response_stream:
            full_response_content += chunk.text

    return {"text": full_response_content}
