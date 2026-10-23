from dashscope import TextGeneration


def normalize_request(input_text):
    return {"model": "qwen-turbo", "prompt": input_text}


def normalize_response(response):
    return response.output.choices[0].message.content
