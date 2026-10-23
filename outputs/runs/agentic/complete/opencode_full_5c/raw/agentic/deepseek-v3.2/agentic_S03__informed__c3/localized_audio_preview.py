import os
import azure.cognitiveservices.speech as speechsdk
from typing import Optional, BinaryIO, Union
from dataclasses import dataclass
from enum import Enum
import tempfile


class VoiceGender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NEUTRAL = "Neutral"


class AudioFormat(str, Enum):
    WAV = "wav"
    MP3 = "mp3"
    OGG = "ogg"


@dataclass
class AudioPreviewConfig:
    voice_name: str
    speaking_rate: float
    pitch: float
    volume: float
    audio_format: AudioFormat


@dataclass
class AudioPreviewResult:
    text: str
    language: str
    audio_data: bytes
    audio_format: AudioFormat
    duration_ms: int
    voice_used: str


class LocalizedAudioPreview:
    def __init__(
        self, speech_key: Optional[str] = None, speech_region: Optional[str] = None
    ):
        self.speech_key = speech_key or os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = speech_region or os.getenv("AZURE_SPEECH_REGION")

        if not self.speech_key:
            raise ValueError("AZURE_SPEECH_KEY environment variable not set")
        if not self.speech_region:
            raise ValueError("AZURE_SPEECH_REGION environment variable not set")

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

    def text_to_speech(
        self,
        text: str,
        language: str,
        voice_name: Optional[str] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        volume: float = 1.0,
        audio_format: AudioFormat = AudioFormat.WAV,
    ) -> AudioPreviewResult:
        if audio_format == AudioFormat.WAV:
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
            )
        elif audio_format == AudioFormat.MP3:
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            )
        elif audio_format == AudioFormat.OGG:
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Ogg16Khz16BitMonoOpus
            )

        if voice_name:
            self.speech_config.speech_synthesis_voice_name = voice_name
        else:
            self._set_default_voice(language)

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )

        ssml = self._create_ssml(text, speaking_rate, pitch, volume)

        try:
            result = synthesizer.speak_ssml_async(ssml).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio_data = result.audio_data

                duration = 0
                if hasattr(result, "audio_duration"):
                    duration = result.audio_duration.total_milliseconds()

                return AudioPreviewResult(
                    text=text,
                    language=language,
                    audio_data=audio_data,
                    audio_format=audio_format,
                    duration_ms=duration,
                    voice_used=self.speech_config.speech_synthesis_voice_name,
                )
            else:
                cancellation_details = speechsdk.CancellationDetails(result)
                raise RuntimeError(
                    f"Speech synthesis failed: {cancellation_details.reason}"
                )

        except Exception as e:
            raise RuntimeError(f"Failed to generate audio preview: {str(e)}")

    def preview_translation(
        self,
        original_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        config: Optional[AudioPreviewConfig] = None,
    ) -> Dict[str, AudioPreviewResult]:
        if config is None:
            config = AudioPreviewConfig(
                voice_name="",
                speaking_rate=1.0,
                pitch=0.0,
                volume=1.0,
                audio_format=AudioFormat.WAV,
            )

        original_audio = self.text_to_speech(
            text=original_text,
            language=source_lang,
            voice_name=config.voice_name,
            speaking_rate=config.speaking_rate,
            pitch=config.pitch,
            volume=config.volume,
            audio_format=config.audio_format,
        )

        translated_audio = self.text_to_speech(
            text=translated_text,
            language=target_lang,
            voice_name=config.voice_name,
            speaking_rate=config.speaking_rate,
            pitch=config.pitch,
            volume=config.volume,
            audio_format=config.audio_format,
        )

        return {"original": original_audio, "translated": translated_audio}

    def save_audio_to_file(
        self, audio_result: AudioPreviewResult, file_path: Optional[str] = None
    ) -> str:
        if file_path is None:
            suffix = f".{audio_result.audio_format.value}"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                file_path = f.name

        with open(file_path, "wb") as f:
            f.write(audio_result.audio_data)

        return file_path

    def _set_default_voice(self, language: str):
        voice_map = {
            "en": "en-US-JennyNeural",
            "es": "es-ES-ElviraNeural",
            "fr": "fr-FR-DeniseNeural",
            "de": "de-DE-KatjaNeural",
            "it": "it-IT-ElsaNeural",
            "ja": "ja-JP-NanamiNeural",
            "zh": "zh-CN-XiaoxiaoNeural",
            "ko": "ko-KR-SunHiNeural",
            "pt": "pt-BR-FranciscaNeural",
            "ru": "ru-RU-SvetlanaNeural",
            "ar": "ar-SA-ZariyahNeural",
        }

        lang_code = language.lower().split("-")[0]
        voice = voice_map.get(lang_code, "en-US-JennyNeural")
        self.speech_config.speech_synthesis_voice_name = voice

    def _create_ssml(self, text: str, rate: float, pitch: float, volume: float) -> str:
        rate_percent = int((rate - 1.0) * 100)
        pitch_st = int(pitch * 100)
        volume_percent = int(volume * 100)

        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.speech_config.speech_synthesis_voice_name[:5]}">
    <voice name="{self.speech_config.speech_synthesis_voice_name}">
        <prosody rate="{rate_percent}%" pitch="{pitch_st}st" volume="{volume_percent}%">
            {text}
        </prosody>
    </voice>
</speak>"""

        return ssml


def create_audio_preview_generator() -> LocalizedAudioPreview:
    return LocalizedAudioPreview()


if __name__ == "__main__":
    preview_generator = LocalizedAudioPreview()

    test_text = "Hello, this is a test of the audio preview system."

    try:
        result = preview_generator.text_to_speech(
            text=test_text, language="en-US", audio_format=AudioFormat.WAV
        )

        print(f"Generated audio preview for: {result.text}")
        print(f"Language: {result.language}")
        print(f"Voice used: {result.voice_used}")
        print(f"Audio format: {result.audio_format.value}")
        print(f"Duration: {result.duration_ms} ms")
        print(f"Audio data size: {len(result.audio_data)} bytes")

    except Exception as e:
        print(f"Error: {str(e)}")
