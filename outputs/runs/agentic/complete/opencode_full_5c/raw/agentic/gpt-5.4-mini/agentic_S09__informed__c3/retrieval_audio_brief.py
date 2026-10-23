from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI()
    prompt = "Summarize these search results as a short spoken brief: " + " | ".join(
        str(item) for item in results
    )
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text
