import os
from openai import AzureOpenAI

def summarize_moderation_decisions(decisions: list[dict], config: dict) -> str:
    client = AzureOpenAI(
        azure_endpoint=config['azure_openai_endpoint'],
        api_key=config['azure_openai_api_key'],
        api_version=config.get('azure_openai_api_version', "2023-05-15"),
    )

    decision_strings = [f"Text: {d['text']}\nCategories: {d['categories']}\nUnsafe: {d['is_unsafe']}" for d in decisions]
    prompt = "Summarize the following moderation decisions:\n" + "\n---\n".join(decision_strings)

    response = client.chat.completions.create(
        model=config['azure_openai_deployment_name'],
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
