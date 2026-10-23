from typing import Optional

from model_client import get_client, resolve_model_name


class PlatformResourceSelector:
    def __init__(self, resource_id: Optional[str] = None):
        self.client = get_client()
        self.resource_id = resource_id or resolve_model_name(None)

    def resolve(self) -> str:
        model = self.client.models.retrieve(self.resource_id)
        return model.id


def select_platform_resource(resource_id: Optional[str] = None) -> str:
    selector = PlatformResourceSelector(resource_id=resource_id)
    return selector.resolve()
