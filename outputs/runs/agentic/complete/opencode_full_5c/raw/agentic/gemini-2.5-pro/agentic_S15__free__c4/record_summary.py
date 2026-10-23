import os
import cohere


def summarize_record(record_text: str):
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    response = co.summarize(
        text=record_text,
        model="summarize-xlarge",
        length="medium",
        extractiveness="medium",
    )

    return response.summary
