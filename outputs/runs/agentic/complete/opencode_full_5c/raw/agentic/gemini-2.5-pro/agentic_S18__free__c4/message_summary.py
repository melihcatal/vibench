import os
import openai
from messaging_models import ProcessingResult

openai.api_key = os.environ.get("OPENAI_API_KEY")


def summarize_results(results: list[ProcessingResult]) -> str:
    """Summarizes a list of message processing results using OpenAI."""
    if not results:
        return "No results to summarize."

    prompt_content = (
        "Summarize the following message processing results in one sentence:\n\n"
    )
    for result in results:
        prompt_content += f"- Message {result.message_id}: {result.status}\n"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_content},
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()
