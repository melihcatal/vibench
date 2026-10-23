from openai import OpenAI


def invoice_summary(text: str, model: str = "gpt-5.4-mini") -> str:
    client = OpenAI()
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Summarize invoice fields concisely."}, {"role": "user", "content": text}])
    return response.choices[0].message.content or ""
