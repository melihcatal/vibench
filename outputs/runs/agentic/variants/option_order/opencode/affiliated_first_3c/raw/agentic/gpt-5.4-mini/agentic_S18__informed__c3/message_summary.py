from openai import OpenAI


def summarize_message_results(results):
    client = OpenAI()
    prompt = f"Summarize these message processing results concisely: {results}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
