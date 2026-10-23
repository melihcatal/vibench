from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI()
    content = " ".join(str(result) for result in results)
    response = client.responses.create(model="gpt-4.1-mini", input=f"Summarize as a spoken brief: {content}")
    return response.output_text
