def normalize_locale(locale):
    if not locale:
        return "en-US"
    return locale.replace("_", "-")


def normalize_voice_request(text=None, ssml=None, locale=None, voice=None, format="mp3"):
    return {
        "text": text,
        "ssml": ssml,
        "locale": normalize_locale(locale),
        "voice": voice,
        "format": format,
    }


def extract_audio_bytes(response):
    if hasattr(response, "read"):
        return response.read()
    if isinstance(response, (bytes, bytearray)):
        return bytes(response)
    if hasattr(response, "content"):
        return response.content
    return response
