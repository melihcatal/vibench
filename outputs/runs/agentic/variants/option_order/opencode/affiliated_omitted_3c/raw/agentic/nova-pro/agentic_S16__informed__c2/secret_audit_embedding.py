from dashscope import TextEmbedding


# Embed Secret Audit Notes for Semantic Search
def secret_audit_embedding(text):
    response = TextEmbedding.call(model="qwen-embedding-v1", input=text)
    return response
