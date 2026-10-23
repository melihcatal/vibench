from openai import OpenAI


def invoice_summary(extracted):
    client = OpenAI()
    content = str(getattr(extracted, "raw", extracted))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Summarize invoice fields briefly."},
            {"role": "user", "content": content},
        ],
    )
    return response.output_text
