from dashscope import Safety


def visual_safety_text(text):
    response = Safety.call(model="qwen-vl", prompt=text)
    return response.output.is_safe
