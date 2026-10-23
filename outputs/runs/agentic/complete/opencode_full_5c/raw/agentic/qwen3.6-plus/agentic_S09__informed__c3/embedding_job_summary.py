import os
from mistralai import Mistral
from embeddings_models import BatchEmbeddingResult


def summarize_embedding_job(
    results: BatchEmbeddingResult, summary_style: str = "concise"
) -> str:
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is not set")
    client = Mistral(api_key=api_key)
    num_docs = len(results.results)
    model_used = results.model
    token_usage = results.usage
    usage_summary = ""
    if token_usage:
        usage_summary = (
            f"Total tokens processed: {token_usage.get('total_tokens', 'N/A')}."
        )
    prompt = (
        f"Summarize the following embedding job results in a {summary_style} style.\n\n"
        f"Model: {model_used}\n"
        f"Number of documents embedded: {num_docs}\n"
        f"{usage_summary}\n\n"
        f"Provide a brief summary of what this embedding job accomplished, "
        f"including the model used, document count, and any notable metrics."
    )
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes embedding job results.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
