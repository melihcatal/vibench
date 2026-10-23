def create_request(model_id, inputs):
    return {
        "model_id": model_id,
        "inputs": inputs,
    }


def create_response(response):
    return {
        "generated_text": response.generated_text,
        "usage": response.usage,
    }
