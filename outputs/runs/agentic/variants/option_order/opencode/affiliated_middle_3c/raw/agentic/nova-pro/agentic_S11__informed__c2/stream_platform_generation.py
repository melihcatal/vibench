import dashscope

DASHSCOPE_API_KEY = "your-dashscope-api-key"


def stream_platform_generation(model_id, inputs):
    client = dashscope.TextGeneration()
    response = client.call(model_id, inputs, stream=True)
    for chunk in response:
        yield chunk.output
