from dashscope import Translation


def alt_text_translate(text, target_language):
    response = Translation.call(
        model="qwen-vl", source_text=text, target_language=target_language
    )
    return response.output.text
