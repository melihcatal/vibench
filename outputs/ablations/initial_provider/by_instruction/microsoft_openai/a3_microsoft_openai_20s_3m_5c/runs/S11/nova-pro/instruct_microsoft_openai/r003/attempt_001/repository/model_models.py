from.model_client import get_client

def normalize_request(prompt):
    return [{"role": "user", "content": prompt}]

def normalize_response(response):
    return response.choices[0].message.content