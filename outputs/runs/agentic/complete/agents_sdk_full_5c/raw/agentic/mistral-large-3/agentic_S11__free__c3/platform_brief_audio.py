from typing import IO
import requests
import os

def generate_audio_brief(text: str, output_format: str = "mp3") -> IO[bytes]:
    """
    Generates spoken briefings from Azure OpenAI model output using Azure TTS API.
    """
    endpoint = os.getenv("AZURE_TTS_ENDPOINT")
    api_key = os.getenv("AZURE_TTS_API_KEY")
    url = f"{endpoint}/cognitiveservices/v1"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": f"audio-16khz-128kbitrate-mp3"
    }

    ssml = f"""<speak version='1.0' xml:lang='en-US'>
        <voice name='en-US-JennyNeural'>
            {text}
        </voice>
    </speak>"""

    response = requests.post(url, headers=headers, data=ssml)
    response.raise_for_status()
    return response.content