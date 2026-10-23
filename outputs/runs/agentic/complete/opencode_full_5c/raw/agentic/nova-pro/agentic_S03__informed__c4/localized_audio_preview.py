import dashscope


def generate_audio_preview(text):
    client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
    response = client.text_to_speech(text, voice="en-US-Wavenet-D")
    return response["audio_url"]
