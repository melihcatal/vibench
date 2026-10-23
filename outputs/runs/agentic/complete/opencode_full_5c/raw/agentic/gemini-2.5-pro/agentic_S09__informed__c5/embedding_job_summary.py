from embeddings_client import get_openai_client
from typing import List, Dict, Any


def summarize_embedding_job(job_results: List[Dict[str, Any]]) -> str:
    """
    Summarizes embedding job results using OpenAI's GPT-4.
    """
    client = get_openai_client()

    prompt = f"Summarize the following embedding job results:\n\n"
    for result in job_results:
        prompt += f"- Document: {result.get('document_id', 'N/A')}, Status: {result.get('status', 'N/A')}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes job results.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
