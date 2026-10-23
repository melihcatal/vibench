import os
from openai import OpenAI

def platform_brief_audio(text: str, voice: str = "alloy", output_filepath: str = "briefing.mp3"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )
    response.stream_to_file(output_filepath)
    return {"status": "success", "output_filepath": output_filepath}
