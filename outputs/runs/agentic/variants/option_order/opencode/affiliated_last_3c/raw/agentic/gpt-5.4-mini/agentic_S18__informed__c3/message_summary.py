from openai import OpenAI


def summarize_message_results(results: list[dict]) -> str:
    client = OpenAI()
    prompt = (
        f"Summarize these message processing results in one short paragraph: {results}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
