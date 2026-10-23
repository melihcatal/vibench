import os
import requests
from xml.etree import ElementTree

def platform_brief_audio(text: str, output_file: str = "output.mp3", voice_name: str = "en-US-JennyNeural") -> str:
    """
    Generates spoken briefings from platform outputs using Azure Cognitive Services Speech (Text-to-Speech).
    """
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION") # e.g., "westus2"

    if not all([speech_key, speech_region]):
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    # Construct the SSML request body
    ssml_body = f"""
<speak version='1.0' xml:lang='en-US'>
    <voice xml:lang='en-US' xml:id='{voice_name}' name='{voice_name}'>
        {text}
    </voice>
</speak>"""

    # Azure Text-to-Speech endpoint
    tts_url = f"https://{speech_region}.tts.speech.microsoft.com/cognitiveservices/v1"

    headers = {
        'Ocp-Apim-Subscription-Key': speech_key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3',
        'User-Agent': 'Python-TTS-Client'
    }

    response = requests.post(tts_url, headers=headers, data=ssml_body.encode('utf-8'))
    response.raise_for_status() # Raise an exception for HTTP errors

    with open(output_file, 'wb') as audio_file:
        audio_file.write(response.content)
        
    return f"Audio generated successfully and saved to {output_file}"
