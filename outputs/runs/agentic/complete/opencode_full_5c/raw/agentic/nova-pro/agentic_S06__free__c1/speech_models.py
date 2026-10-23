def normalize_request(text, output_format="mp3", voice_id="Joanna"):
    return {"Text": text, "OutputFormat": output_format, "VoiceId": voice_id}


def normalize_response(response):
    return response["AudioStream"].read()
