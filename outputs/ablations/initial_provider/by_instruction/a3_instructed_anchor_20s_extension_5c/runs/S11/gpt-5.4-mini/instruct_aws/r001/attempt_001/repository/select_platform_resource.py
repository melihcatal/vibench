from model_client import select_bedrock_resource


def select_platform_resource(preferred_model: str = None) -> str:
    return select_bedrock_resource(preferred_model)
