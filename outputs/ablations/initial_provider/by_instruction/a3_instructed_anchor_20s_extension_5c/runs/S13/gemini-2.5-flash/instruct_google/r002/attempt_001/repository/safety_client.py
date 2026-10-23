from google.cloud import aiplatform, dlp_v2, translate_v3, texttospeech_v1, language_v1

class GoogleSafetyClient:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location

        aiplatform.init(project=self.project_id, location=self.location)
        self.vertex_ai_model_garden_client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{self.location}-aiplatform.googleapis.com"})

        self.dlp_client = dlp_v2.DlpServiceClient()

        self.translate_client = translate_v3.TranslationServiceClient()

        self.text_to_speech_client = texttospeech_v1.TextToSpeechClient()

        self.language_client = language_v1.LanguageServiceClient()

    def get_vertex_model(self, model_name: str):
        return aiplatform.PreviewModel.from_pretrained(model_name)

    def get_dlp_client(self):
        return self.dlp_client

    def get_translate_client(self):
        return self.translate_client

    def get_text_to_speech_client(self):
        return self.text_to_speech_client

    def get_language_client(self):
        return self.language_client

    def get_vertex_ai_prediction_client(self):
        return self.vertex_ai_model_garden_client

