import os
import requests
from xml.etree import ElementTree

def platform_brief_audio(text_output, output_filename, config=None):
    config = config or {}
    key = os.environ.get("AZURE_TTS_KEY", config.get("key"))
    endpoint = os.environ.get("AZURE_TTS_ENDPOINT", config.get("endpoint")) # e.g., https://<region>.tts.speech.microsoft.com/

    if not all([key, endpoint]):
        raise ValueError("Azure Text-to-Speech key and endpoint must be provided.")

    path = 'cognitiveservices/v1'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-24khz-16bit-mono-pcm',
        'User-Agent': 'python-client'
    }

    # Example SSML for a neutral voice
    # You can customize voice, style, etc. based on Azure TTS documentation
    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice.set('name', 'en-US-JennyNeural') # Example voice, choose an appropriate one
    voice.text = text_output
    
    xml_body = ElementTree.tostring(body)

    response = requests.post(constructed_url, headers=headers, data=xml_body)

    if response.status_code == 200:
        with open(output_filename, 'wb') as audio_file:
            audio_file.write(response.content)
        return {"audio_file": output_filename, "text": text_output, "status": "success"}
    else:
        raise Exception(f"Azure TTS failed with status code {response.status_code}: {response.text}")
