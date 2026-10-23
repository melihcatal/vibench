from typing import List, Dict, Any
from openai import AzureOpenAI
from safety_models import ModerationResponse

def summarize_moderation_decisions(moderation_results: List[ModerationResponse], config: Dict[str, Any] = None) -> str:
    config = config or {}
    # Azure OpenAI Configuration
    # Environment variables should be set for AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION
    # or passed via config. Here we use config for consistency.
    
    client = AzureOpenAI(
        azure_endpoint = config.get("azure_openai_endpoint"),
        api_key = config.get("azure_openai_api_key"),
        api_version = config.get("azure_openai_api_version", "2024-02-01"), # Use a recent stable API version
    )

    # Prepare the input for summarization
    summary_input = "The following are moderation decisions for various text inputs:\n\n"
    for i, result in enumerate(moderation_results):
        summary_input += f"Message {i+1}:\n"
        summary_input += f"  Text: {result.text[:100]}...\n" # Truncate long texts
        summary_input += f"  Decision: {result.decision}\n"
        summary_input += f"  Categories: {result.categories}\n\n"
    
    # Prompt for summarization
    prompt = f"Please provide a concise summary of the moderation decisions. Highlight any overall trends or significant findings.\n\n{summary_input}"
    
    try:
        response = client.chat.completions.create(
            model=config.get("azure_openai_deployment_name", "gpt-35-turbo"), # Example deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes moderation decisions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing moderation decisions: {e}"
