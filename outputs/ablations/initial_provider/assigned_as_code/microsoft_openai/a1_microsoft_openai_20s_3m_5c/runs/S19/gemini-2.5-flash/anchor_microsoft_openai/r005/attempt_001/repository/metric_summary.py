import os
from openai import AzureOpenAI

def metric_summary(payload, config=None):
    config = config or {}
    client = AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-15-preview"
    )

    metric_data_str = str(payload.get('metric_data'))
    prompt = f"Summarize the following metric data and highlight any trends or anomalies: {metric_data_str}"

    response = client.chat.completions.create(
        model=config.get('azure_openai_model', 'gpt-4o'),
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes metric data."},
            {"role": "user", "content": prompt}
        ]
    )
    return {'summary': response.choices[0].message.content}
