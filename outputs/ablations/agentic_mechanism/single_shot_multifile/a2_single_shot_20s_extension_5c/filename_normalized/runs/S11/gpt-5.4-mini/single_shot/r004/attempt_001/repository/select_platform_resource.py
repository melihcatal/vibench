from typing import Optional

from model_client import get_config
from model_models import PlatformResourceSelection



def select_platform_resource(resource_hint: Optional[str] = None) -> PlatformResourceSelection:
    config = get_config()
    resource_id = resource_hint or config.resource_id or config.model_id
    return PlatformResourceSelection(provider=config.provider, resource_id=resource_id, model_id=config.model_id, deployment_id=config.deployment_id)
