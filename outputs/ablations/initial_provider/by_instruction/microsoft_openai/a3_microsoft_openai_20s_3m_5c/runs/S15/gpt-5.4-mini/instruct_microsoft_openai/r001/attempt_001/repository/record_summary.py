from openai import OpenAI


def summarize_record(record):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Summarize document records briefly."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.output_text
