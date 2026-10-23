import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def synthesize_text(text):
    response = dashscope.CosyVoice.synthesize(text=text)
    return response.audio_content
