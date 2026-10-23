from dashscope import TextEmbedding


# Summarize Secret Rotation Status
def rotation_summary(text):
    response = TextEmbedding.call(model="qwen-embedding-v1", input=text)
    return response
