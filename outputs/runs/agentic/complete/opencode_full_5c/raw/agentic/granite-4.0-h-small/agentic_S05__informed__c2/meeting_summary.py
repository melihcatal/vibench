import requests, json


def summarize_meeting(transcript_chunk):
    """Summarize live meeting transcript chunks using Mistral Chat API."""
    endpoint = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer MISTRAL_API_KEY",
        "Content-Type": "application/json",
    }
    prompt = f"Summarize the meeting so far:\n{transcript_chunk}"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
    }
    r = requests.post(endpoint, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


# Example usage: summarize_meeting('...meeting transcript...')
