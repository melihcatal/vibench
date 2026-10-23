from invoke_platform_model import invoke_platform_model


import openai


def generate_briefing(output):
    response = openai.Audio.create(
        input=output,
        model='tts-1',
        voice='alloy'
    )
    return response['url']