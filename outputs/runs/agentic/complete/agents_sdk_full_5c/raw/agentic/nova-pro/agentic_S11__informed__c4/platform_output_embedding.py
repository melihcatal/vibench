OPENAI_API_KEY')
    response = openai.Embedding.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']