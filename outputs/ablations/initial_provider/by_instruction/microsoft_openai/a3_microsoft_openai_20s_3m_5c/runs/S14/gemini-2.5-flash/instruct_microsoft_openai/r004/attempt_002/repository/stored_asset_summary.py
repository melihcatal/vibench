import os
from openai import AzureOpenAI

def summarize_text(text: str, max_tokens: int = 150):
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not azure_endpoint or not api_key or not deployment_name:
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables must be set.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary, "full_response": response.model_dump_json()}
    except Exception as e:
        return {"error": f"Summarization failed: {e}"}
