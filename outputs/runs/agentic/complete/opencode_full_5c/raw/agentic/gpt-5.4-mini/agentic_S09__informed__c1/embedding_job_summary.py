from openai import OpenAI


def summarize_embedding_job(results):
    client = OpenAI()
    prompt = f"Summarize this embedding job result set concisely: {results}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
