from speech_client import get_polly_client


def select_voice(language_code=None, config=None):
    config = config or {}
    client = get_polly_client(region_name=config.get("region"))
    if language_code:
        response = client.describe_voices(LanguageCode=language_code)
    else:
        response = client.describe_voices()
    voices = [{
        "id": voice["Id"],
        "name": voice["Name"],
        "gender": voice["Gender"],
        "language_code": voice["LanguageCode"]
    } for voice in response["Voices"]]
    return {"voices": voices}
