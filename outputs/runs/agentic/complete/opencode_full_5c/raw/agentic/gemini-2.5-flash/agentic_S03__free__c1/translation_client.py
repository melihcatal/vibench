from google.cloud import translate_v2 as translate
from google.cloud import language_v2 as language
from google.cloud import texttospeech
from google.cloud import aiplatform
import os


class TranslationClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.translate_client = translate.Client()
        self.language_client = language.LanguageServiceClient()
        self.text_to_speech_client = texttospeech.TextToSpeechClient()

        # Initialize Vertex AI for embeddings
        aiplatform.init(project=project_id, location="us-central1")
        self.embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(
            "textembedding-gecko@001"
        )

    def translate_text(
        self, text: str, target_language: str, source_language: str = None
    ) -> str:
        result = self.translate_client.translate(
            text, target_language=target_language, source_language=source_language
        )
        return result["translatedText"]

    def batch_translate_texts(
        self, texts: list[str], target_language: str, source_language: str = None
    ) -> list[str]:
        translations = []
        for text in texts:
            result = self.translate_client.translate(
                text, target_language=target_language, source_language=source_language
            )
            translations.append(result["translatedText"])
        return translations

    def translate_html(
        self, html: str, target_language: str, source_language: str = None
    ) -> str:
        result = self.translate_client.translate(
            html,
            target_language=target_language,
            source_language=source_language,
            format_="html",
        )
        return result["translatedText"]

    def analyze_sentiment(self, text: str, language: str):
        document = language.Document(
            content=text, type_=language.Document.Type.PLAIN_TEXT
        )
        response = self.language_client.analyze_sentiment(
            document=document, encoding_type=language.EncodingType.UTF8
        )
        return response.document_sentiment

    def classify_text(self, text: str):
        document = language.Document(
            content=text, type_=language.Document.Type.PLAIN_TEXT
        )
        response = self.language_client.classify_text(document=document)
        return response.categories

    def get_text_embeddings(self, text_segments: list[str]):
        embeddings = self.embedding_model.get_embeddings(text_segments)
        return [embedding.values for embedding in embeddings]

    def synthesize_speech(
        self,
        text: str,
        language_code: str,
        voice_name: str = None,
        ssml_gender: str = None,
    ) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_selection_params = texttospeech.VoiceSelectionParams(
            language_code=language_code
        )
        if voice_name:
            voice_selection_params.name = voice_name
        if ssml_gender:
            voice_selection_params.ssml_gender = texttospeech.SsmlVoiceGender[
                ssml_gender
            ]

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.text_to_speech_client.synthesize_speech(
            input=synthesis_input,
            voice=voice_selection_params,
            audio_config=audio_config,
        )
        return response.audio_content
