def normalize_request(text):
    return {"input": text, "model": "text-embedding-ada-002"}


def normalize_response(response):
    return response.data[0].embedding
