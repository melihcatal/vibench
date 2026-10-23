import dashscope

def stream_completion(prompt):
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    response = dashscope.Text.completion(prompt=prompt, model='qwen-turbo', stream=True)
    for chunk in response:
        yield chunk.output.text