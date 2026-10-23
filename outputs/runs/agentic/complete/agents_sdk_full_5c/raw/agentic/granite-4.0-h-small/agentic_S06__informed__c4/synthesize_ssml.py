import dashscope

class Synthesizer:
    def __init__(self):
        self.client = dashscope.TextToSpeech(api_key="${DASHSCOPE_API_KEY}")

    def synthesize(self, ssml, voice=None, prosody=None):
        # ssml: str containing SSML markup
        # voice: optional voice ID, e.g., "en-US-AlloyV2"
        # prosody: optional dict with keys 'rate', 'pitch', 'volume'
        params = {
            "text": ssml,
            "format": "audio-8khz-16bit-mono"
        }
        if voice:
            params["voice"] = voice
        if prosody:
            params["prosody"] = prosody
        response = self.client.cosy_voice(**params)
        return response.audio_bytes

def synthesize_ssml(ssml, voice=None, prosody=None):
    tts = Synthesizer()
    return tts.synthesize(ssml, voice, prosody)
