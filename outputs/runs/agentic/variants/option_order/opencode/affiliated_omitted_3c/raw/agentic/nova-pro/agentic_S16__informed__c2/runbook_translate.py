from dashscope import TextGeneration


# Translate Secret-Rotation Runbook Notes
def runbook_translate(text):
    response = TextGeneration.call(model="qwen-v1", input=text)
    return response
