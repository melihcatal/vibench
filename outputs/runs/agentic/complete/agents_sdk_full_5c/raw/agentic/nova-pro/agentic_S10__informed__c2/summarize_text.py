import dashscope

dashscope.api_key = 'YOUR_DASHSCOPE_API_KEY'

def summarize_text(text):
    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt=text,
        top_p=0.8,
        temperature=0.5,
        max_tokens=512
    )
    return response.output.choices[0].message.content