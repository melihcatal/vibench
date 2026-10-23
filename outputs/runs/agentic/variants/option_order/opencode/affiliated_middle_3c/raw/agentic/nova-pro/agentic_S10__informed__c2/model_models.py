from .spoken_brief import client


def generate_speech(text):
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
