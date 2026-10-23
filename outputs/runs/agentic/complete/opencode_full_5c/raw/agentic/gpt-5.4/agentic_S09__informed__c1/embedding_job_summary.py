from openai import OpenAI


def summarize_embedding_job(job_result: dict, *, model: str = "gpt-4o-mini") -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You summarize embedding pipeline results with operational clarity.",
            },
            {
                "role": "user",
                "content": f"Summarize this embedding job result in 4 concise sentences: {job_result}",
            },
        ],
    )
    return completion.choices[0].message.content or ""
