import dashscope

def summarize_text(text):
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    response = dashscope.Text.summarization(text=text, model='qwen-turbo')
    return response.output.text