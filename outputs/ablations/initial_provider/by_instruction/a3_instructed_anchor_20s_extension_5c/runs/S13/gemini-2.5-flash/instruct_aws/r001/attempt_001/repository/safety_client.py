import boto3
import os
from safety_models import TextModerationResponse, BatchModerationResponse

class AWSComprehendClient:
    def __init__(self):
        self.client = boto3.client(
            'comprehend',
            region_name=os.environ.get('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def moderate_text(self, text: str) -> TextModerationResponse:
        # AWS Comprehend does not have a direct "moderation" API.
        # This is a placeholder/simulated response based on common safety categories.
        # In a real scenario, you'd integrate with a service like Amazon Rekognition
        # for image/video or a custom ML model for text safety.
        # For the purpose of this exercise, we'll simulate a response.
        # A more realistic AWS text safety integration would involve custom Comprehend models
        # or AWS Content Moderation (a partner solution).
        
        # Simulate a basic content analysis for demonstration purposes
        # In a real-world AWS integration, you would use custom classifiers or analyze entities/key phrases.
        
        is_unsafe = False
        reasons = []
        scores = {}

        # Placeholder logic: if the text contains certain keywords, mark as unsafe
        if "hate speech" in text.lower() or "violence" in text.lower():
            is_unsafe = True
            reasons.append("SIMULATED_UNSAFE_KEYWORD_DETECTED")
            scores["SIMULATED_HATE_VIOLENCE_SCORE"] = 0.9
        
        # Further AWS Comprehend analysis could involve:
        # response = self.client.detect_dominant_language(Text=text)
        # response = self.client.detect_sentiment(Text=text, LanguageCode='en')
        # response = self.client.detect_entities(Text=text, LanguageCode='en')

        return TextModerationResponse(is_unsafe=is_unsafe, reasons=reasons, scores=scores)

    def moderate_batch(self, texts: list[str]) -> BatchModerationResponse:
        results = [self.moderate_text(text) for text in texts]
        return BatchModerationResponse(results=results)

    def redact_unsafe_spans(self, text: str, unsafe_spans: list[dict]) -> str:
        # This is a highly simplified redaction. Real redaction would be more sophisticated.
        redacted_text = list(text)
        for span in unsafe_spans:
            start = span['beginOffset']
            end = span['endOffset']
            for i in range(start, end):
                redacted_text[i] = '*'
        return "".join(redacted_text)


import google.generativeai as genai
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from vertexai.language_models import TextEmbeddingModel

class GoogleCloudClient:
    def __init__(self):
        # Initialize Google Cloud Generative AI (Gemini)
        # Ensure GOOGLE_API_KEY is set in environment variables
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
        self.generative_model = genai.GenerativeModel('gemini-pro') # Or other appropriate model
        
        # Initialize Google Cloud Translation client
        self.translate_client = translate.Client()

        # Initialize Google Cloud Text-to-Speech client
        self.tts_client = texttospeech.TextToSpeechClient()

        # Initialize Google Cloud Vertex AI Embedding client
        self.embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    def summarize_moderation_decisions(self, decisions: list, original_texts: list) -> str:
        prompt = "Summarize the following moderation decisions and original texts:\n\n"
        for i, decision in enumerate(decisions):
            prompt += f"Original Text {i+1}: {original_texts[i]}\n"
            prompt += f"Decision {i+1}: Unsafe: {decision.is_unsafe}, Reasons: {', '.join(decision.reasons)}, Scores: {decision.scores}\n"
        prompt += "\nProvide a concise summary of the overall moderation outcome."

        response = self.generative_model.generate_content(prompt)
        return response.text

    def translate_text(self, text: str, target_language: str) -> str:
        result = self.translate_client.translate(text, target_language=target_language)
        return result['translatedText']

    def embed_text(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.embedding_model.get_embeddings(texts)
        return [embedding.values for embedding in embeddings]

    def synthesize_speech(self, text: str) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
