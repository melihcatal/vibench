import azure.cognitiveservices.speech as speechsdk
import os


class LanguageAwareStreamer:
    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        if not self.speech_key or not self.speech_region:
            raise ValueError(
                "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
            )

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

    def create_recognizer_with_language(
        self, language_code="en-US", enable_punctuation=True, enable_dictation=False
    ):
        self.speech_config.speech_recognition_language = language_code
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestPunctuation,
            "true" if enable_punctuation else "false",
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps,
            "true",
        )

        if enable_dictation:
            self.speech_config.enable_dictation()

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        return recognizer

    def start_streaming_with_settings(
        self, language_code="en-US", enable_punctuation=True, enable_dictation=False
    ):
        recognizer = self.create_recognizer_with_language(
            language_code, enable_punctuation, enable_dictation
        )

        results = []

        def recognizing_callback(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
                results.append(
                    {
                        "type": "interim",
                        "text": evt.result.text,
                        "language": language_code,
                        "has_punctuation": enable_punctuation,
                    }
                )

        def recognized_callback(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                results.append(
                    {
                        "type": "final",
                        "text": evt.result.text,
                        "language": language_code,
                        "has_punctuation": enable_punctuation,
                        "result_id": evt.result.result_id,
                    }
                )

        recognizer.recognizing.connect(recognizing_callback)
        recognizer.recognized.connect(recognized_callback)

        recognizer.start_continuous_recognition_async()

        return recognizer, results

    def get_supported_languages(self):
        return {
            "en-US": "English (United States)",
            "en-GB": "English (United Kingdom)",
            "es-ES": "Spanish (Spain)",
            "fr-FR": "French (France)",
            "de-DE": "German (Germany)",
            "it-IT": "Italian (Italy)",
            "ja-JP": "Japanese",
            "ko-KR": "Korean",
            "zh-CN": "Chinese (Mandarin, Simplified)",
            "zh-TW": "Chinese (Mandarin, Traditional)",
            "pt-BR": "Portuguese (Brazil)",
            "ru-RU": "Russian",
            "ar-SA": "Arabic (Saudi Arabia)",
            "hi-IN": "Hindi (India)",
        }

    def validate_language_code(self, language_code):
        supported = self.get_supported_languages()
        return language_code in supported

    def create_streaming_recognizer(
        self,
        language_code="en-US",
        punctuation=True,
        word_timestamps=True,
        profanity_filter="masked",
    ):
        if not self.validate_language_code(language_code):
            raise ValueError(f"Unsupported language code: {language_code}")

        self.speech_config.speech_recognition_language = language_code
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestPunctuation,
            "true" if punctuation else "false",
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps,
            "true" if word_timestamps else "false",
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_ProfanityOption, profanity_filter
        )

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )

        return recognizer
