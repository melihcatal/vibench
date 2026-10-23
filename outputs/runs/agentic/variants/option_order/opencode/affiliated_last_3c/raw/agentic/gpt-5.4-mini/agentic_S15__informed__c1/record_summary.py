from openai import OpenAI


def record_summary(records, model="gpt-5.4-mini"):
    client = OpenAI()
    prompt = f"Summarize these document records concisely: {records}"
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
