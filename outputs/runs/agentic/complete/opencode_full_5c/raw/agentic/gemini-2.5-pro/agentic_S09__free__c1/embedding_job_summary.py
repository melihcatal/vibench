import os
import openai


def summarize_embedding_job(job_results_text: str) -> str:
    """
    Summarizes embedding job results using OpenAI's GPT-3.5 Turbo.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following embedding job results:\n\n{job_results_text}",
            },
        ],
    )

    if response.choices:
        return response.choices[0].message.content.strip()
    return ""
