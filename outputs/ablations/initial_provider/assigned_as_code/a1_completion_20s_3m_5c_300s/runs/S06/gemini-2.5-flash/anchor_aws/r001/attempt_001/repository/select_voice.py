import boto3


def select_voice(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    language_code = payload.get("language_code")
    
    if language_code:
        response = client.describe_voices(LanguageCode=language_code)
    else:
        response = client.describe_voices()
        
    voices = response.get("Voices", [])
    
    # Optionally, filter by gender or other attributes if provided in payload
    gender = payload.get("gender")
    if gender:
        voices = [voice for voice in voices if voice.get("Gender") == gender]

    # Return voice IDs and names
    return {"voices": [{
        "id": voice["Id"],
        "name": voice["Name"],
        "gender": voice["Gender"],
        "language_code": voice["LanguageCode"]
    } for voice in voices]}
