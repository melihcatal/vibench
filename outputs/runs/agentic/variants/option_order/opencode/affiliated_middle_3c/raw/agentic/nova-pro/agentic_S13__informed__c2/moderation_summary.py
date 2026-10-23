from dashscope import TextGeneration


def moderation_summary(text):
    api_key = "DASHSCOPE_API_KEY"
    response = TextGeneration.call(model="qwen", api_key=api_key, text=text)
    return response.output
