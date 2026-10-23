from dashscope import TextToSpeech

DASHSCOPE_API_KEY = 'your_dashscope_api_key'

def generate_brief_audio(text):
    client = TextToSpeech(api_key=DASHSCOPE_API_KEY)
    response = client.synthesize(text=text, voice='en-US-Wavenet-D')
    return response.audio_content