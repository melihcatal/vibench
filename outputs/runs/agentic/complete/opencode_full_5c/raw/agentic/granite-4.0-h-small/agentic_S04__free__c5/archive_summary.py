import json

# provider: OpenAI ChatGPT (summarization)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1/chat/completions"


def archive_summary(transcripts):
    """
    Summarizes a list of transcript strings into a concise archival summary.
    Uses OpenAI's Chat Completions with a system prompt.
    Returns the summary string.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Summarize the following meeting transcripts into a brief, professional summary (max 150 words).",
        },
        {"role": "user", "content": "\n\n".join(transcripts)},
    ]
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": "gpt-4o-mini", "messages": messages, "temperature": 0}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
