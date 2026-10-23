import os
import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def summarize_meeting_chunk(text: str):
    response = co.summarize(
        text=text, model="command", length="short", extractiveness="low"
    )
    return response.summary
