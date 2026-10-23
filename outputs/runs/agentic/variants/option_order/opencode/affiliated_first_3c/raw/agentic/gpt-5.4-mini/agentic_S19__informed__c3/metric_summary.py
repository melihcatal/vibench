from openai import OpenAI


def metric_summary(points, model: str = 'gpt-5.4-mini') -> str:
    client = OpenAI()
    response = client.chat.completions.create(model=model, messages=[{'role': 'system', 'content': 'Summarize metric trends and anomalies.'}, {'role': 'user', 'content': str(points)}])
    return response.choices[0].message.content or ''
