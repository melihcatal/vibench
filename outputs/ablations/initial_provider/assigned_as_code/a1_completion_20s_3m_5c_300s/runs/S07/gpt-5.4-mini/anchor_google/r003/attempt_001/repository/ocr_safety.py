from openai import OpenAI


def ocr_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.responses.create(
        model=config.get("model", "gpt-5.4-mini"),
        input=[
            {
                "role": "system",
                "content": "Assess whether the OCR text contains unsafe content and respond with a short verdict.",
            },
            {"role": "user", "content": payload["text"]},
        ],
    )
    return {"assessment": response.output_text}
