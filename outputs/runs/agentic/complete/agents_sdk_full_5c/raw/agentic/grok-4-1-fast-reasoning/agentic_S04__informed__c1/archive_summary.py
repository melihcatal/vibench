import os
from mistralai.client import MistralClient

def archive_summary(transcript):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required.")
    client = MistralClient(api_key=api_key)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that creates concise summaries of meeting transcripts."},
        {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript}"}
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content