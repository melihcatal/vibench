def create_request(model, messages):
    return {"model": model, "messages": messages}


def parse_response(response):
    return response.json()["choices"][0]["message"]["content"]
