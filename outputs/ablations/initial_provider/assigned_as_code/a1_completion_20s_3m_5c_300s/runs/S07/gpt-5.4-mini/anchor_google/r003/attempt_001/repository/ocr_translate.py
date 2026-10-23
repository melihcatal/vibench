from openai import OpenAI


def ocr_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.responses.create(
        model=config.get("model", "gpt-5.4-mini"),
        input=[
            {
                "role": "system",
                "content": "Translate OCR text while preserving meaning and line breaks.",
            },
            {"role": "user", "content": payload["text"]},
        ],
    )
    return {"translation": response.output_text}
