import dashscope

class Synthesizer:
    def __init__(self):
        self.client = dashscope.TextToSpeech(api_key="${DASHSCOPE_API_KEY}")
    def synthesize(self, text):
        response = self.client.cosy_voice(text=text, model_id="default")
        return response.audio_bytes

def synthesize_text(text):
    tts = Synthesizer()
    return tts.synthesize(text)
