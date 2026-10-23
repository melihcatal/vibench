from dashscope import Generation

def generate_invoice_summary(text):
    response = Generation.call(model='qwen-turbo', messages=[{'role': 'user', 'content': text}])
    return response.output.choices[0].message.content