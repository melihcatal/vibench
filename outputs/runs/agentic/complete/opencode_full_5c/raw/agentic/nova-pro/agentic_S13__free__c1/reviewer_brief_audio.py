import safety_client


def generate_reviewer_brief(text):
    client = safety_client.get_client()
    audio_brief = client.generate_audio(text)
    return audio_brief
