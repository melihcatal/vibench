import os
import xml.etree.ElementTree as ET
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

# Azure Speech TTS configuration
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


# Helper function to create SSML with voice/prosody settings
# Refer to Azure TTS documentation for available voice names per locale.
xml_template = """<?xml version="1.0"?>
<speech xmlns="http://www.w3.org/2001/10/synthesis">
  <!-- Define the voice and prosody attributes -->
  <voice name="{voice}">
    <prosody rate="{rate}" pitch="{pitch}" volume="{volume}">{text}</prosody>
  </voice>
</speech>"""


def synthesize_ssml(ssml_xml: str, output_file: str = None) -> bytes:
    """Synthesize SSML to an audio byte stream using Azure Speech TTS.

    Args:
        ssml_xml (str): Valid SSML string containing <speech> root element.
        output_file (str, optional): Path to save the audio file. If omitted, returns audio bytes.

    Returns:
        bytes: Synthesized speech bytes.
    """
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    speech_config.speech_synthesis_output_format = "Riff24Khz16BitMonoPcm"
    audio_config = AudioConfig(output_format="Riff24Khz16BitMonoPcm")
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Parse SSML XML safely
    try:
        root = ET.fromstring(ssml_xml)
        voice_name = root.attrib.get("name")
        rate = root.find(".//prosody").attrib.get("rate", "default")
        pitch = root.find(".//prosody").attrib.get("pitch", "default")
        volume = root.find(".//prosody").attrib.get("volume", "default")
        text = root.find(".//").text or ""
    except ET.ParseError:
        raise ValueError("Invalid SSML structure")

    speech_config.speech_synthesis_voice_name = voice_name or "en-US-JennyNeural"
    synthesizer.speech_configuration.speech_synthesis_voice_name = voice_name
    result = synthesizer.speak_ssml_async(ssml_xml).get()
    audio_bytes = result.audio_data
    if output_file:
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes


# Example usage (kept in comments only)
# ssml = '<speech xmlns="http://www.w3.org/2001/10/synthesis">' \
# '<voice name="en-US-JennyNeural"><prosody rate=\"slow\">Hello world!</prosody></voice>' \
# '</speech>'
# audio = synthesize_ssml(ssml)
