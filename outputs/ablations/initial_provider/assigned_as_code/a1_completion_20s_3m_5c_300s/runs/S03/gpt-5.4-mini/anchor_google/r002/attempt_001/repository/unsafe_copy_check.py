from openai import OpenAI


def unsafe_copy_check(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=payload["text"],
    )
    return {"unsafe": "unsafe" in response.output_text.lower(), "analysis": response.output_text}
