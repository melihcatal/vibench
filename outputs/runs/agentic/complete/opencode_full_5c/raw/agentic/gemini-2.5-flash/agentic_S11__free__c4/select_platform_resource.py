from model_client import get_text_generation_model


def select_platform_resource(model_name: str = "gemini-pro"):
    model = get_text_generation_model(model_name=model_name)
    return model
