from invoke_platform_model import invoke_platform_model


import openai


def embed_output(output):
    response = openai.Embedding.create(input=output, model='text-embedding-ada-002')
    return response['data'][0]['embedding']