from openai import OpenAI


def metric_summary(metric_name, series):
    client = OpenAI()
    prompt = f"Summarize recent trends and anomalies for {metric_name} using these points: {series}"
    completion = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
