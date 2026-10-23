import dashscope


def summarize_record(text: str):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    response = dashscope.Generation.call(
        model="qwen-turbo",
        prompt=f"Summarize the following text: {text}",
    )
    return response.output.choices[0].message.content
