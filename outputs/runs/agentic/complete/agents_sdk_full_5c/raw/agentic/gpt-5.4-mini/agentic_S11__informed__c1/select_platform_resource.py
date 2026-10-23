from typing import Optional

from model_client import build_azure_openai_client, load_platform_config


class PlatformResourceSelector:
    def __init__(self, deployment: Optional[str] = None):
        self.config = load_platform_config()
        if deployment:
            self.config = self.config.__class__(
                endpoint=self.config.endpoint,
                api_key=self.config.api_key,
                api_version=self.config.api_version,
                deployment=deployment,
            )
        self.client = build_azure_openai_client(self.config)

    def resolve_deployment(self) -> str:
        return self.config.deployment

    def resolve_client(self):
        return self.client


def select_platform_resource(deployment: Optional[str] = None) -> str:
    return PlatformResourceSelector(deployment=deployment).resolve_deployment()
