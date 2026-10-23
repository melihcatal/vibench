from model_client import get_azure_openai_client
from model_models import ModelRequest, ModelResult, normalize_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: ModelRequest) -> ModelResult:
    client = get_azure_openai_client()
    resource = select_platform_resource()
    deployment = request.model or resource["deployment"]
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    text = normalize_text(response.choices[0].message.content)
    return ModelResult(text=text, model=deployment, resource_id=resource["resource_id"], usage=getattr(response, "usage", None), raw=response)
