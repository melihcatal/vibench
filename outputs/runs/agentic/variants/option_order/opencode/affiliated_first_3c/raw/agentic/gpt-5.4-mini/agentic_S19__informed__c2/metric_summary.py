import os

from openai import OpenAI


def metric_summary(metric_name, datapoints, model="gpt-5.4-mini"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize recent trends and anomalies for {metric_name} from these datapoints: {datapoints}"
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
