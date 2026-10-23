import os
import cohere


def onboarding_summary(text_to_summarize: str) -> str:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.summarize(
        text=text_to_summarize, model="command", length="medium", extractiveness="low"
    )

    return response.summary
