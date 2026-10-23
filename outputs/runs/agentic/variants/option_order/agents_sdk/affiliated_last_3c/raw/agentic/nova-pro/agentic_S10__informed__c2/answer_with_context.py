import dashscope

def answer_with_context(question, context):
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    response = dashscope.Text.qa(question=question, context=context, model='qwen-turbo')
    return response.output.answer