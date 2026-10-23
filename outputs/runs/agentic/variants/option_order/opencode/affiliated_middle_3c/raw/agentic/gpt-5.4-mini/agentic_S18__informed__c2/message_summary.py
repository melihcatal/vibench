from openai import OpenAI


def summarize_message_processing(results: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Summarize message processing results:\n{results}"
    )
    return response.output_text
