from model_client import get_default_platform_resource
from model_models import GenerationRequest, PlatformResource


def select_platform_resource(request: GenerationRequest) -> PlatformResource:
    resource = get_default_platform_resource()
    if request.max_tokens > 4000 and resource.model_family == "gpt-4o-mini":
        return PlatformResource(
            deployment_name="gpt-4o",
            azure_deployment="gpt-4o",
            model_family="gpt-4o",
        )
    return resource
