import requests


def reviewer_brief_audio(text: str) -> str:
    url = "https://api.aws.amazon.com/polly"
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "AWSPolly.SynthesizeSpeech",
    }
    payload = {"Text": text, "OutputFormat": "mp3", "VoiceId": "Joanna"}
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY")),
    )
    return response.content
