from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI()
    brief = " ".join(str(item) for item in results)
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=brief
    )
    return response


if __name__ == "__main__":
    print(retrieval_audio_brief(["Result one", "Result two"]))
