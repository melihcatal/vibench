from model_client import create_openai_client, load_config, resolve_model
from model_models import (
    TranslateRequest,
    TranslateResponse,
    build_system_message,
    build_user_message,
)


def translate_text(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
) -> TranslateResponse:
    req = TranslateRequest(
        text=text,
        target_language=target_language,
        source_language=source_language,
        model=model,
        temperature=temperature,
    )
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    if req.source_language == "auto":
        lang_instruction = "Detect the source language automatically."
    else:
        lang_instruction = f"The source language is {req.source_language}."

    system_prompt = (
        f"You are a professional translator. {lang_instruction} "
        f"Translate the following text into {req.target_language}. "
        "Preserve the original meaning, tone, and formatting. "
        "Return only the translated text with no explanations."
    )

    messages = [
        build_system_message(system_prompt),
        build_user_message(req.text),
    ]

    response = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        max_tokens=max(1024, len(req.text) // 2),
        temperature=req.temperature,
    )

    translated = response.choices[0].message.content.strip()
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return TranslateResponse(
        translated_text=translated,
        detected_language=req.source_language,
        target_language=req.target_language,
        model=response.model,
        usage=usage,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read() if not sys.stdin.isatty() else ""
    target = sys.argv[1] if len(sys.argv) > 1 else "en"
    if input_text:
        result = translate_text(input_text, target_language=target)
        print(result.translated_text)
