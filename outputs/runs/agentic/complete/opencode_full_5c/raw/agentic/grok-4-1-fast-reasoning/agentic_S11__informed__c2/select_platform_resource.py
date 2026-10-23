def select_platform_resource(model_family: str) -> str:
    model_mapping = {
        "gemini-pro": "gemini-1.5-pro",
        "gemini-flash": "gemini-1.5-flash",
        "gemini": "gemini-1.5-flash",
    }
    return model_mapping.get(model_family, model_family)
