import os

from openai import AzureOpenAI


def platform_output_safety(text: str) -> dict:
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )
    prompt = f"Assess whether the following output is unsafe, toxic, or disallowed. Return strict JSON with keys safe and reasons. Output: {text}"
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return {
        "provider": "azure-openai",
        "raw": response,
        "text": response.choices[0].message.content,
    }
