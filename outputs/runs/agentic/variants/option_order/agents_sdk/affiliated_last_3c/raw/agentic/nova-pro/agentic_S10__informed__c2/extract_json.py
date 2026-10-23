import dashscope

def extract_json(text):
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    response = dashscope.Text.extraction(text=text, model='qwen-turbo')
    return response.output.choices[0].text