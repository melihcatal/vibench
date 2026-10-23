from openai import OpenAI

from embeddings_client import embeddings_base_url, embeddings_api_key


def retrieval_audio_brief(results):
    client = OpenAI(api_key=embeddings_api_key(), base_url=embeddings_base_url())
    prompt = "Summarize these retrieval results as a short spoken brief: " + str(results)
    return client.responses.create(model="gpt-5.4-mini", input=prompt)
