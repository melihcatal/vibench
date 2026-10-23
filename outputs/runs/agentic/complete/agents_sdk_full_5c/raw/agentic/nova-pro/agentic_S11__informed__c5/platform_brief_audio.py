import elevenlabs

def generate_audio(text):
    client = elevenlabs.Client(api_key='your-elevenlabs-api-key')
    audio = client.generate(text=text, voice='Bella')
    elevenlabs.save(audio, 'output.mp3')