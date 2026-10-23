def normalize_text(text):
    if text is None:
        return ""
    return " ".join(str(text).split())


def normalize_locale(locale):
    if not locale:
        return None
    return str(locale).replace("_", "-")


def build_text_request(text, voice_id=None, output_format=None, engine=None):
    request = {"Text": normalize_text(text), "TextType": "text"}
    if voice_id:
        request["VoiceId"] = voice_id
    if output_format:
        request["OutputFormat"] = output_format
    if engine:
        request["Engine"] = engine
    return request


def build_ssml_request(ssml, voice_id=None, output_format=None, engine=None):
    request = {"Text": ssml, "TextType": "ssml"}
    if voice_id:
        request["VoiceId"] = voice_id
    if output_format:
        request["OutputFormat"] = output_format
    if engine:
        request["Engine"] = engine
    return request


def response_audio_bytes(response):
    return response["AudioStream"].read()
