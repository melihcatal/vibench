def create_request(model_family: str, prompt: str) -> dict:
    return {'model_family': model_family, 'prompt': prompt}

def process_response(response: dict) -> str:
    return response.get('output', '')

def normalize_output(output: str) -> str:
    return output.strip().replace('\n', ' ')"