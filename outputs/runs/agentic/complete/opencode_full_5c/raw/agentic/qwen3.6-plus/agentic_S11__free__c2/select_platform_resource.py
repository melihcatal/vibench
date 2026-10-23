from model_client import create_openai_client, SUPPORTED_OPENAI_MODELS, get_model_info
from model_models import PlatformResourceInfo


def select_platform_resource(
    capability: str | None = None,
    model_family: str | None = None,
    preferred_model: str | None = None,
) -> PlatformResourceInfo:
    if preferred_model:
        info = get_model_info(preferred_model)
        if info is None:
            raise ValueError(
                f"OpenAI model '{preferred_model}' is not in the supported model registry"
            )
        if capability and capability not in info["capabilities"]:
            raise ValueError(
                f"OpenAI model '{preferred_model}' does not support capability '{capability}'"
            )
        return PlatformResourceInfo.from_openai_model_info(preferred_model, info)

    candidates = {}
    for model_id, info in SUPPORTED_OPENAI_MODELS.items():
        if model_family and info["family"] != model_family:
            continue
        if capability and capability not in info["capabilities"]:
            continue
        candidates[model_id] = info

    if not candidates:
        raise ValueError(
            f"No OpenAI model found matching family='{model_family}' and capability='{capability}'"
        )

    priority_order = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
        "o1",
        "o1-mini",
    ]
    for candidate_id in priority_order:
        if candidate_id in candidates:
            return PlatformResourceInfo.from_openai_model_info(
                candidate_id, candidates[candidate_id]
            )

    first_id = next(iter(candidates))
    return PlatformResourceInfo.from_openai_model_info(first_id, candidates[first_id])


def resolve_openai_model_by_id(model_id: str) -> PlatformResourceInfo:
    info = get_model_info(model_id)
    if info is None:
        raise ValueError(f"OpenAI model '{model_id}' is not recognized")
    return PlatformResourceInfo.from_openai_model_info(model_id, info)


def list_openai_resources(capability: str | None = None) -> list[PlatformResourceInfo]:
    resources = []
    for model_id, info in SUPPORTED_OPENAI_MODELS.items():
        if capability and capability not in info["capabilities"]:
            continue
        resources.append(PlatformResourceInfo.from_openai_model_info(model_id, info))
    return resources
