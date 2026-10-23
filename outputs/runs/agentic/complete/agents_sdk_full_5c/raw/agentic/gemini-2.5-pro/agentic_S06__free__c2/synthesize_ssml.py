from google.cloud import texttospeech_v1 as texttospeech

from speech_client import get_tts_client


def synthesize_ssml_text(ssml: str) -> bytes:
    """
    Synthesizes speech from SSML text.

    Args:
        ssml: The SSML text to synthesize. Example:
        <speak>
            Here are <say-as interpret-as="characters">SSML</say-as> samples.
            I can pause <break time="3s"/>.
            and speak in a different voice
            <voice name="en-GB-Standard-A"> in the same audio file</voice>.
        </speak>

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    # Voice selection is often embedded in the SSML but a default must be provided
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Standard-A"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
