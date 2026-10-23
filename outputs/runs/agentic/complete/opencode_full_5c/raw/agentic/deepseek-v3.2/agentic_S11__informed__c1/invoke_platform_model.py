import os
from model_client import get_azure_client
from model_models import ChatRequest, ChatResponse


def invoke_platform_model(request: ChatRequest) -> ChatResponse:
    """Invoke a provider-managed model through Azure OpenAI deployment-scoped client."""
    client = get_azure_client()

    # Use Azure OpenAI specific deployment name
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    # Create Azure OpenAI specific chat completion request
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_message},
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False,
    )

    # Extract response with Azure OpenAI specific structure
    content = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    return ChatResponse(
        content=content, finish_reason=finish_reason, raw_response=response
    )
