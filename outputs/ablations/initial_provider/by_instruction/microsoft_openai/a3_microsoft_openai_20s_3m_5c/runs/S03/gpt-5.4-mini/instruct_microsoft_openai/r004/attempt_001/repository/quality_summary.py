from openai import OpenAI


def quality_summary(translations):
    client = OpenAI()
    response = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "system", "content": "Summarize translation quality issues concisely."}, {"role": "user", "content": str(translations)}])
    return response.choices[0].message.content or ""
