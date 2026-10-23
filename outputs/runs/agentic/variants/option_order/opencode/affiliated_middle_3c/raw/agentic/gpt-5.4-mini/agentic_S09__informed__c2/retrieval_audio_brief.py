from openai import OpenAI


def main(results: list[str]) -> str:
    client = OpenAI()
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input="; ".join(results)
    )
    return response.model_dump_json() if hasattr(response, "model_dump_json") else ""
