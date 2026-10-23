import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def select_voice(locale):
    voices = dashscope.CosyVoice.list_voices(locale=locale)
    return voices
