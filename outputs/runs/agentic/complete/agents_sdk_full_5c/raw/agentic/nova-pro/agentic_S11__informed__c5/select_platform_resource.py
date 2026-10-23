import dashscope

def select_resource():
    dashscope.api_key = 'your-dashscope-api-key'
    response = dashscope.TextGeneration.call(model='qwen-turbo', prompt='Hello, world!')
    print(response)