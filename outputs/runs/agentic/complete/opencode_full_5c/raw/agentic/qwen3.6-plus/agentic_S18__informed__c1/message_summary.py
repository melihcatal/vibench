import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL_ID = "gpt-4"


def summarize_processing_results(results: list[dict]) -> str:
    summary_input = json.dumps(results, indent=2)
    prompt = (
        f"Summarize the following message processing results in a concise paragraph. "
        f"Include key metrics, success/failure counts, and any notable patterns:\n\n{summary_input}"
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a messaging analytics assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def summarize_single_message(message_data: dict) -> str:
    prompt = (
        f"Provide a one-sentence summary of this message payload:\n\n"
        f"{json.dumps(message_data, indent=2)}"
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize message payloads concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()
