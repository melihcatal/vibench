import dashscope

DASHSCOPE_API_KEY = "your-dashscope-api-key"


def invoke_platform_model(model_id, inputs):
    client = dashscope.TextGeneration()
    response = client.call(model_id, inputs)
    return response.output
