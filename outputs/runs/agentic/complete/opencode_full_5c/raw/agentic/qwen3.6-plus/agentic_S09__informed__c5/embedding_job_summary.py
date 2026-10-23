import os
import json
from openai import OpenAI


def summarize_embedding_job(embedding_results, model="gpt-4o", api_key=None):
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    if isinstance(embedding_results, dict):
        summary_input = json.dumps(embedding_results, default=str)
    elif isinstance(embedding_results, list):
        summary_input = json.dumps(
            {
                "total_embeddings": len(embedding_results),
                "sample_results": embedding_results[:5],
            },
            default=str,
        )
    else:
        summary_input = str(embedding_results)
    prompt = (
        "Summarize the following embedding job results. "
        "Include the total number of embeddings, the model used, "
        "token usage statistics, and any notable patterns in the data. "
        "Provide a concise summary.\n\n"
        f"Embedding job results:\n{summary_input}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content
