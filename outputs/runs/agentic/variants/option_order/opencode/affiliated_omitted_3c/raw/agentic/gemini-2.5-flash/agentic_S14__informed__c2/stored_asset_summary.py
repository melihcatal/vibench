import os
from openai import AzureOpenAI


def summarize_content(text_content: str, max_tokens: int = 150) -> str:
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
    azure_openai_deployment_name = os.getenv(
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"
    )  # e.g., gpt-35-turbo

    if (
        not azure_openai_endpoint
        or not azure_openai_key
        or not azure_openai_deployment_name
    ):
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variables must be set."
        )

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-15-preview",  # Use a compatible API version
    )

    try:
        response = client.chat.completions.create(
            model=azure_openai_deployment_name,  # model = "deployment_name"
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text: {text_content}",
                },
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing content: {e}"
