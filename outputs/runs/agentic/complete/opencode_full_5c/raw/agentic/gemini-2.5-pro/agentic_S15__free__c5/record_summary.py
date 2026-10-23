import os
import cohere


def record_summary(text: str):
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.summarize(
        text=text, model="command", length="medium", extractiveness="medium"
    )

    return response.summary
