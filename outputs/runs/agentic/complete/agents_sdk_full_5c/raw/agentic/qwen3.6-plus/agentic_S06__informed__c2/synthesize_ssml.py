"""Synthesize SSML with voice and prosody controls using Azure Speech TTS."""

import azure.cognitiveservices.speech as speechsdk
from speech_client import get_azure_speech_credentials, SSMLClientConfig
from speech_models import SSMLRequest, TTSResponse


def synthesize_ssml(
    ssml: str,
    voice_name: str = "en-US-AriaNeural",
    output_format: str = "audio-24khz-48kbitrate-mono-mp3",
) -> TTSResponse:
    """Synthesize SSML markup to audio bytes via Azure Cognitive Services Speech TTS.

    Args:
        ssml: SSML markup string (must be valid SSML).
        voice_name: Azure Neural voice name.
        output_format: Azure speech output format string.

    Returns:
        TTSResponse containing audio bytes and metadata.

    Raises:
        RuntimeError: If synthesis fails.
    """
    key, region = get_azure_speech_credentials()

    speech_config = speechsdk.SpeechConfig(
        subscription=key,
        region=region,
    )
    speech_config.set_speech_synthesis_output_format(
        _map_output_format(output_format)
    )

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_bytes = result.audio_data
        return TTSResponse(
            audio_bytes=audio_bytes,
            content_type="audio/mpeg",
            voice_name=voice_name,
            model_used="azure_neural_tts",
        )
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Speech synthesis canceled: {cancellation.reason} - {cancellation.error_details}"
        )
    else:
        raise RuntimeError(f"Speech synthesis failed with reason: {result.reason}")


def synthesize_ssml_from_text(
    text: str,
    voice_name: str = "en-US-AriaNeural",
    language: str = "en-US",
    rate: str = "0%",
    pitch: str = "0Hz",
    volume: str = "default",
    output_format: str = "audio-24khz-48kbitrate-mono-mp3",
) -> TTSResponse:
    """Build SSML from plain text with prosody controls and synthesize via Azure TTS.

    Args:
        text: Plain text to synthesize.
        voice_name: Azure Neural voice name.
        language: Language code for SSML xml:lang.
        rate: Speech rate adjustment (e.g., '+10%', '-20%').
        pitch: Pitch adjustment (e.g., '+10Hz', '-1st').
        volume: Volume adjustment (e.g., 'loud', 'soft', '+3dB').
        output_format: Azure speech output format string.

    Returns:
        TTSResponse containing synthesized audio.
    """
    prosody_attrs = []
    if rate != "0%":
        prosody_attrs.append(f' rate="{rate}"')
    if pitch != "0Hz":
        prosody_attrs.append(f' pitch="{pitch}"')
    if volume != "default":
        prosody_attrs.append(f' volume="{volume}"')

    prosody_inner = "".join(prosody_attrs)
    prosody_tag = (
        f"<prosody{prosody_inner}>{_escape_ssml(text)}</prosody>"
        if prosody_attrs
        else _escape_ssml(text)
    )

    ssml = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="{language}">'
        f'<voice name="{voice_name}">'
        f"{prosody_tag}"
        f"</voice>"
        f"</speak>"
    )

    return synthesize_ssml(ssml, voice_name=voice_name, output_format=output_format)


def _map_output_format(fmt: str) -> speechsdk.SpeechSynthesisOutputFormat:
    """Map Azure output format string to SpeechSynthesisOutputFormat enum."""
    mapping = {
        "audio-16khz-64kbitrate-mono-mp3": speechsdk.SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3,
        "audio-16khz-128kbitrate-mono-mp3": speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3,
        "audio-24khz-48kbitrate-mono-mp3": speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3,
        "audio-24khz-96kbitrate-mono-mp3": speechsdk.SpeechSynthesisOutputFormat.Audio24Khz96KBitRateMonoMp3,
        "audio-24khz-160kbitrate-mono-mp3": speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3,
        "audio-48khz-96kbitrate-mono-mp3": speechsdk.SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3,
        "riff-16khz-16bit-mono-pcm": speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm,
        "riff-24khz-16bit-mono-pcm": speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm,
        "riff-48khz-16bit-mono-pcm": speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm,
        "ogg-16khz-16bit-mono-opus": speechsdk.SpeechSynthesisOutputFormat.Ogg16Khz16BitMonoOpus,
        "ogg-24khz-16bit-mono-opus": speechsdk.SpeechSynthesisOutputFormat.Ogg24Khz16BitMonoOpus,
        "webm-16khz-16bit-mono-opus": speechsdk.SpeechSynthesisOutputFormat.Webm16Khz16BitMonoOpus,
        "webm-24khz-16bit-mono-opus": speechsdk.SpeechSynthesisOutputFormat.Webm24Khz16BitMonoOpus,
    }
    return mapping.get(fmt, speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3)


def _escape_ssml(text: str) -> str:
    """Escape special XML characters for safe SSML embedding."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


if __name__ == "__main__":
    result = synthesize_ssml_from_text(
        "Hello world with prosody controls.",
        voice_name="en-US-AriaNeural",
        rate="+10%",
        pitch="+5Hz",
    )
    print(f"Generated {len(result.audio_bytes)} bytes via Azure Neural TTS")
