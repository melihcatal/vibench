import dashscope

DASHSCOPE_API_KEY = "your-dashscope-api-key"


def collect_platform_metadata(model_id, inputs):
    client = dashscope.TextGeneration()
    response = client.call(model_id, inputs)
    return response.output, response.metadata
