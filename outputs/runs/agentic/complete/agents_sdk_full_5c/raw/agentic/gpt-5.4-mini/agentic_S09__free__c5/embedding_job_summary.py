from collections import Counter

from embeddings_client import get_client, OPENAI_CHAT_MODEL


def embedding_job_summary(job_records):
    client = get_client()
    counts = Counter(record.get("status", "unknown") for record in job_records)
    prompt = {
        "role": "user",
        "content": f"Summarize this OpenAI embedding job result distribution: {dict(counts)}. Keep it concise.",
    }
    completion = client.chat.completions.create(model=OPENAI_CHAT_MODEL, messages=[prompt])
    return {
        "status_counts": dict(counts),
        "summary": completion.choices[0].message.content,
        "provider": "openai",
    }
