from openai import AzureOpenAI

class SpeechClient:
    def __init__(self, api_key, endpoint):
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint)

    def synthesize_text(self, text, voice='en-US-JennyNeural'):
        response = self.client.audio.speech.create(
            model=voice,
            input=text
        )
        return response.content

    def synthesize_ssml(self, ssml, voice='en-US-JennyNeural'):
        response = self.client.audio.speech.create(
            model=voice,
            input=ssml,
            input_type='ssml'
        )
        return response.content

    def list_voices(self):
        response = self.client.audio.speech.list_voices()
        return response.content

    def save_audio(self, audio_data, file_path):
        with open(file_path, 'wb') as f:
            f.write(audio_data)