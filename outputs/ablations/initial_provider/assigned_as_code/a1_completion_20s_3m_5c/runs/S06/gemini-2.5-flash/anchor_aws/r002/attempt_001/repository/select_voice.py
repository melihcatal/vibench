from speech_client import get_polly_client

def select_voice(payload, config=None):
    config = config or {}
    client = get_polly_client(region_name=config.get("region"))
    language_code = payload.get("language_code", "en-US")
    voices = []
    paginator = client.get_paginator('describe_voices')
    for page in paginator.paginate(LanguageCode=language_code):
        voices.extend(page['Voices'])
    
    # Optional filtering by gender if needed by payload
    if "gender" in payload:
        gender_filter = payload["gender"].capitalize()
        voices = [voice for voice in voices if voice.get("Gender") == gender_filter]

    return {"voices": voices}
