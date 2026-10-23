import dashscope

DASHSCOPE_API_KEY = "your-dashscope-api-key"


def platform_output_embedding(text):
    client = dashscope.TextEmbedding()
    response = client.call(text)
    return response.output
