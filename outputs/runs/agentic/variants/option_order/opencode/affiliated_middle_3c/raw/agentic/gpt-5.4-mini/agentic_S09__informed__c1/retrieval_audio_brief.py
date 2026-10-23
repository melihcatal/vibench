from openai import OpenAI


def generate_retrieval_audio_brief(results: list[dict], model: str = 'gpt-4.1-mini') -> str:
    client = OpenAI()
    prompt = 'Create a concise spoken brief from these search results: ' + str(results)
    response = client.audio.speech.create(model='gpt-4o-mini-tts', voice='alloy', input=prompt)
    return response
