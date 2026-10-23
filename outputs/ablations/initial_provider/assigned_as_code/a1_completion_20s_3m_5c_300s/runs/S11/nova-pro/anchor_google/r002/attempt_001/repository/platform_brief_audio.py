from google import genai

def generate_brief_audio(response):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    audio = client.text_to_speech.synthesize(response.text)
    return audio.audio_content