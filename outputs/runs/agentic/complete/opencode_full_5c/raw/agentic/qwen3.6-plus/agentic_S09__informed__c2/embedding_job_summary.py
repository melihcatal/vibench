import os
import openai
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def summarize_embedding_job(embedding_results, model="gpt-4o-mini"):
    client = get_openai_client()

    total_embeddings = len(embedding_results)
    total_tokens = sum(
        r.get("usage", {}).get("total_tokens", 0) for r in embedding_results
    )
    models_used = set(r.get("model", "unknown") for r in embedding_results)

    summary_text = (
        f"Embedding job summary: {total_embeddings} texts embedded, "
        f"{total_tokens} total tokens consumed, "
        f"models used: {', '.join(sorted(models_used))}."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You summarize embedding job results concisely.",
            },
            {"role": "user", "content": summary_text},
        ],
    )

    return {
        "total_embeddings": total_embeddings,
        "total_tokens": total_tokens,
        "models_used": list(models_used),
        "summary": response.choices[0].message.content,
    }
