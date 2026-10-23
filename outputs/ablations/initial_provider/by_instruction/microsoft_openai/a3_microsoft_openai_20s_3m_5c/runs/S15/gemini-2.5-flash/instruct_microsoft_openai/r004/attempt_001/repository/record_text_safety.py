import os
from openai import AzureOpenAI
from typing import Dict, Any, List

def check_text_safety(text_fields: List[str]) -> Dict[str, Any]:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") # e.g., gpt-4o

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_deployment_name]):
        raise ValueError("Azure OpenAI environment variables not set. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT_NAME.")

    openai_client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-15-preview" # Example API version
    )

    # OpenAI provides content moderation APIs or can be prompted for safety checks
    # For simplicity, we'll use a chat completion to ask if content is unsafe
    # In a real scenario, consider using a dedicated moderation endpoint if available and suitable.
    
    safety_results = {}
    for i, text in enumerate(text_fields):
        response = openai_client.chat.completions.create(
            model=azure_openai_deployment_name, 
            messages=[
                {"role": "system", "content": "You are a content moderation assistant. Determine if the following text is unsafe, offensive, or inappropriate. Respond with 'safe' or 'unsafe' and a brief reason if unsafe."},
                {"role": "user", "content": f"Analyze this text: {text}"}
            ]
        )
        result = response.choices[0].message.content
        safety_results[f"field_{i}"] = {"text": text, "moderation_result": result}
    
    return safety_results
