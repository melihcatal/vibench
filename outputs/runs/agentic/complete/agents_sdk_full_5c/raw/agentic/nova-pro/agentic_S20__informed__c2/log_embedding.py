from dashscope import Embedding

def embed_message(message):
    response = Embedding.call(
        model='text-embedding-ada-002',
        input=message
    )
    return response.output.embedding

if __name__ == '__main__':
    embedding = embed_message('Hello, world!')
    print(embedding)