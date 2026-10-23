from elevenlabs import Client


def generate_briefing(text):
    client = Client(api_key=os.getenv("ELEVENLABS_API_KEY"))
    response = client.text_to_speech(text=text, voice="Bella")
    return response.audio_url
