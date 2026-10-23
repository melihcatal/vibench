from openai import OpenAI

from messaging_client import openai_endpoint, openai_model


def message_summary(results):
    client = OpenAI(base_url=openai_endpoint())
    text = "\n".join([str(result) for result in results])
    response = client.responses.create(model=openai_model(), input=text)
    return {"provider": "openai", "model": openai_model(), "summary": response.output_text}
