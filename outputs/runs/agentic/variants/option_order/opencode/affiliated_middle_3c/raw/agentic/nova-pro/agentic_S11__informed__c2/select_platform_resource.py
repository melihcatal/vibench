import dashscope

DASHSCOPE_API_KEY = "your-dashscope-api-key"


def select_platform_resource(model_family):
    client = dashscope.TextGeneration()
    models = client.list_models(model_family)
    return models
