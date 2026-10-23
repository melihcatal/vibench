from model_models import CompletionRequest, CompletionResponse
from model_client import get_azure_openai_client
from openai import AzureOpenAI

def collect_azure_openai_metadata(request: CompletionRequest, deployment_name: str = "gpt-35-turbo") -> CompletionResponse:
    client = get_azure_openai_client()
    try:
        response = client.chat.completions.create(
            model=deployment_name, 
            messages=[{"role": "user", "content": request.prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        text_output = response.choices[0].message.content if response.choices else ""
        metadata = {
            "id": response.id,
            "model": response.model,
            "usage": response.usage.model_dump() if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "total_tokens": response.usage.total_tokens if response.usage else None
        }
        return CompletionResponse(text=text_output, provider_response=metadata)
    except AzureOpenAI as e: raise RuntimeError(f"Azure OpenAI API error: {e}")