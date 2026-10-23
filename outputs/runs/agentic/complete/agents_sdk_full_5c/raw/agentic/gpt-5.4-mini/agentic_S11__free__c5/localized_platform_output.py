from model_client import create_platform_client


# Provider-identifying signal: OpenAI translations through Responses API.
def translate_platform_output(output_text: str, target_locale: str = "es") -> str:
    client = create_platform_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": f"Translate the following text into {target_locale}."},
            {"role": "user", "content": output_text},
        ],
    )
    return getattr(response, "output_text", "") or ""
