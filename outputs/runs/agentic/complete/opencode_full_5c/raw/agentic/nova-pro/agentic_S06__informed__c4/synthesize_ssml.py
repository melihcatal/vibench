import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def synthesize_ssml(ssml):
    response = dashscope.CosyVoice.synthesize(ssml=ssml)
    return response.audio_content
