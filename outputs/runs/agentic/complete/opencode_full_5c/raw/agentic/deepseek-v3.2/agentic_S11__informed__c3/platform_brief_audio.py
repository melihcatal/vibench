import azure.cognitiveservices.speech as speechsdk
import os
import tempfile
from typing import Dict, Any, Optional, BinaryIO
from pathlib import Path


class AzureSpeechTTS:
    """Text-to-Speech using Azure AI Speech Service."""

    def __init__(
        self, speech_key: Optional[str] = None, speech_region: Optional[str] = None
    ):
        self.speech_key = speech_key or os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = speech_region or os.getenv("AZURE_SPEECH_REGION")

        if not self.speech_key:
            raise ValueError("AZURE_SPEECH_KEY environment variable is required")
        if not self.speech_region:
            raise ValueError("AZURE_SPEECH_REGION environment variable is required")

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

    def synthesize_to_file(
        self,
        text: str,
        output_path: Optional[str] = None,
        voice_name: str = "en-US-JennyNeural",
        output_format: str = "Audio24Khz96KBitRateMonoMp3",
    ) -> Dict[str, Any]:
        """
        Synthesize text to audio file.
        """
        if not output_path:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"tts_{os.urandom(8).hex()}.mp3")

        self.speech_config.speech_synthesis_voice_name = voice_name
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat[output_format]
        )

        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        try:
            result = synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                file_size = (
                    Path(output_path).stat().st_size
                    if Path(output_path).exists()
                    else 0
                )

                return {
                    "text": text,
                    "audio_file": output_path,
                    "file_size_bytes": file_size,
                    "voice": voice_name,
                    "format": output_format,
                    "provider": "azure_speech",
                    "success": True,
                    "metadata": {
                        "result_id": result.result_id,
                        "duration": getattr(result, "audio_duration", None),
                    },
                }
            else:
                cancellation_details = speechsdk.CancellationDetails(result)
                return {
                    "text": text,
                    "error": cancellation_details.error_details,
                    "reason": str(cancellation_details.reason),
                    "voice": voice_name,
                    "provider": "azure_speech",
                    "success": False,
                }

        except Exception as e:
            return {
                "text": text,
                "error": str(e),
                "voice": voice_name,
                "provider": "azure_speech",
                "success": False,
            }

    def synthesize_to_stream(
        self,
        text: str,
        voice_name: str = "en-US-JennyNeural",
        output_format: str = "Audio24Khz96KBitRateMonoMp3",
    ) -> Dict[str, Any]:
        """
        Synthesize text to audio stream.
        """
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat[output_format]
        )

        stream = speechsdk.audio.PushAudioOutputStream()
        audio_config = speechsdk.audio.AudioOutputConfig(stream=stream)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        try:
            result = synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio_data = stream.get_audio_data()

                return {
                    "text": text,
                    "audio_data": audio_data,
                    "data_size_bytes": len(audio_data),
                    "voice": voice_name,
                    "format": output_format,
                    "provider": "azure_speech",
                    "success": True,
                    "metadata": {
                        "result_id": result.result_id,
                        "duration": getattr(result, "audio_duration", None),
                    },
                }
            else:
                cancellation_details = speechsdk.CancellationDetails(result)
                return {
                    "text": text,
                    "error": cancellation_details.error_details,
                    "reason": str(cancellation_details.reason),
                    "voice": voice_name,
                    "provider": "azure_speech",
                    "success": False,
                }

        except Exception as e:
            return {
                "text": text,
                "error": str(e),
                "voice": voice_name,
                "provider": "azure_speech",
                "success": False,
            }

    def get_available_voices(
        self, locale: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get available voices from Azure Speech Service.
        """
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

        try:
            result = synthesizer.get_voices_async().get()

            voices = []
            for voice in result.voices:
                voice_info = {
                    "name": voice.short_name,
                    "locale": voice.locale,
                    "gender": voice.gender.name
                    if hasattr(voice.gender, "name")
                    else str(voice.gender),
                    "voice_type": voice.voice_type.name
                    if hasattr(voice.voice_type, "name")
                    else str(voice.voice_type),
                    "styles": voice.style_list if hasattr(voice, "style_list") else [],
                    "sample_rate_hz": voice.sample_rate_hz
                    if hasattr(voice, "sample_rate_hz")
                    else None,
                }

                if locale and voice.locale != locale:
                    continue

                voices.append(voice_info)

            return voices

        except Exception as e:
            print(f"Error getting voices: {e}")
            return []

    def get_voice_characteristics(self, voice_name: str) -> Dict[str, Any]:
        """
        Get detailed characteristics of a specific voice.
        """
        voices = self.get_available_voices()

        for voice in voices:
            if voice["name"] == voice_name:
                return voice

        return {}


def generate_audio_briefing(
    text: str,
    output_path: Optional[str] = None,
    voice: str = "en-US-JennyNeural",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> Dict[str, Any]:
    """
    Generate spoken briefing from platform output using Azure Speech TTS.
    """
    tts = AzureSpeechTTS()

    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        <voice name="{voice}">
            <prosody rate="{speaking_rate}" pitch="{pitch}Hz">
                {text}
            </prosody>
        </voice>
    </speak>
    """

    result = tts.synthesize_to_file(ssml_text, output_path, voice)

    if result.get("success"):
        result["ssml_used"] = True
        result["speaking_rate"] = speaking_rate
        result["pitch"] = pitch

    return result


def generate_multilingual_briefing(
    text: str, locale: str = "en-US", output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate briefing with locale-appropriate voice.
    """
    tts = AzureSpeechTTS()

    voice_map = {
        "en-US": "en-US-JennyNeural",
        "en-GB": "en-GB-SoniaNeural",
        "es-ES": "es-ES-ElviraNeural",
        "fr-FR": "fr-FR-DeniseNeural",
        "de-DE": "de-DE-KatjaNeural",
        "it-IT": "it-IT-ElsaNeural",
        "ja-JP": "ja-JP-NanamiNeural",
        "zh-CN": "zh-CN-XiaoxiaoNeural",
        "zh-TW": "zh-TW-HsiaoChenNeural",
    }

    voice = voice_map.get(locale, "en-US-JennyNeural")

    return generate_audio_briefing(text, output_path, voice)


def create_briefing_from_model_response(
    model_response: Dict[str, Any],
    include_metadata: bool = False,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create audio briefing from a model response.
    """
    text = model_response.get("text", "")

    if include_metadata:
        metadata = model_response.get("metadata", {})
        metadata_summary = "\n\nAdditional details: " + str(metadata)
        text += metadata_summary

    briefing_result = generate_audio_briefing(text, output_path)

    combined_result = model_response.copy()
    combined_result["audio_briefing"] = briefing_result

    return combined_result
