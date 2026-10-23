from typing import List
import requests
import os
import base64


class AzureSpeechSynthesizer:
    def __init__(self):
        self.api_key = os.getenv("AZURE_SPEECH_KEY")
        self.region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        self.url = (
            f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        )
        if not self.api_key:
            raise ValueError("AZURE_SPEECH_KEY environment variable must be set")

    def synthesize_speech(
        self, text: str, language: str, voice: str = "en-US-JennyNeural"
    ) -> bytes:
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        }
        ssml = f"""<speak version='1.0' xml:lang='{language}'>
            <voice name='{voice}'>
                {text}
            </voice>
        </speak>"""
        response = requests.post(self.url, headers=headers, data=ssml.encode("utf-8"))
        response.raise_for_status()
        return response.content


def generate_spoken_previews(texts: List[str], target_language: str) -> List[Dict]:
    synthesizer = AzureSpeechSynthesizer()
    previews = []
    for text in texts:
        audio_content = synthesizer.synthesize_speech(text, target_language)
        previews.append(
            {
                "text": text,
                "audio_preview": base64.b64encode(audio_content).decode("utf-8"),
                "format": "mp3",
            }
        )
    return previews
