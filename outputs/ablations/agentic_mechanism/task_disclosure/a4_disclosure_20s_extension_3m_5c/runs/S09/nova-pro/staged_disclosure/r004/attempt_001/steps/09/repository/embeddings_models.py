from amazon_bedrock import DirectEmbeddingsClient

def create_embeddings_request(text):
    return {
        'inputText': text,
        'modelId': 'amazon.titan-embed-text-v1'
    }

def process_embeddings_response(response):
    return response['embedding']

def normalize_embeddings(embedding):
    return [float(x) for x in embedding]