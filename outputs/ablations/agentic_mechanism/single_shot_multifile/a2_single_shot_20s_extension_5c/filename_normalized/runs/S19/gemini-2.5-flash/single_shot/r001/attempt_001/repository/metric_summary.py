import os
from openai import OpenAI

def summarize_metric_trends(metric_data: list, prompt_prefix: str = "Summarize the following metric data:") -> str:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    # Convert metric_data to a string format suitable for LLM input
    data_str = []
    for item in metric_data:
        data_str.append(f"Timestamp: {item.get('timestamp')}, Value: {item.get('value')}, Labels: {item.get('resource_labels', item.get('dimensions'))}")
    
    full_prompt = f"{prompt_prefix}\n\n{'\n'.join(data_str)}"

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes metric trends and identifies anomalies."},
            {"role": "user", "content": full_prompt}
        ]
    )

    return completion.choices[0].message.content