import os
import vertexai
from google.cloud import dlp_v2
from vertexai.preview.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
from typing import List, Dict, Any

class SafetyClient:
    _vertex_ai_initialized = False
    _dlp_client = None

    def __init__(self, project_id: str = None, location: str = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

        self._initialize_vertex_ai()

    def _initialize_vertex_ai(self):
        if not SafetyClient._vertex_ai_initialized:
            vertexai.init(project=self.project_id, location=self.location)
            SafetyClient._vertex_ai_initialized = True

    def get_generative_model(self, model_name: str = "gemini-pro") -> GenerativeModel:
        self._initialize_vertex_ai()
        return GenerativeModel(model_name)

    def get_dlp_client(self) -> dlp_v2.DlpServiceClient:
        if SafetyClient._dlp_client is None:
            SafetyClient._dlp_client = dlp_v2.DlpServiceClient()
        return SafetyClient._dlp_client

    def moderate_text_with_vertex_ai(self, text: str, model_name: str = "gemini-pro") -> dict:
        model = self.get_generative_model(model_name)
        response = model.generate_content(
            [text],
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False,
        )

        safety_ratings = []
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'safety_ratings'):
                    for rating in candidate.safety_ratings:
                        safety_ratings.append({
                            "category": rating.category.name,
                            "probability": rating.probability.name,
                            "blocked": rating.blocked
                        })

        return {"safety_ratings": safety_ratings}
