from openai import OpenAI


def document_field_extraction(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.responses.create(
        model=config.get("model", "gpt-5.4-mini"),
        input=[
            {
                "role": "system",
                "content": "Extract structured fields from normalized OCR text as concise JSON-like text.",
            },
            {"role": "user", "content": payload["text"]},
        ],
    )
    return {"fields": response.output_text}
