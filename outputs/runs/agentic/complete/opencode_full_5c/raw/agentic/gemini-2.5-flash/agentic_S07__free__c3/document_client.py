import os
from google.cloud import vision
from google.cloud import documentai_v1 as documentai
from google.cloud import translate
from google.cloud import aiplatform


class GoogleCloudClients:
    _vision_client = None
    _documentai_client = None
    _translation_client = None
    _vertex_ai_client = None
    _vertex_ai_model_garden_client = None

    @classmethod
    def get_vision_client(cls):
        if cls._vision_client is None:
            cls._vision_client = vision.ImageAnnotatorClient()
        return cls._vision_client

    @classmethod
    def get_documentai_client(cls):
        if cls._documentai_client is None:
            cls._documentai_client = documentai.DocumentProcessorServiceClient()
        return cls._documentai_client

    @classmethod
    def get_translation_client(cls):
        if cls._translation_client is None:
            cls._translation_client = translate.TranslationServiceClient()
        return cls._translation_client

    @classmethod
    def get_vertex_ai_client(cls):
        if cls._vertex_ai_client is None:
            project_id = os.environ.get("GOOGLE_PROJECT_ID")
            location = os.environ.get("GOOGLE_LOCATION")
            if not project_id or not location:
                raise ValueError(
                    "GOOGLE_PROJECT_ID and GOOGLE_LOCATION environment variables must be set."
                )
            aiplatform.init(project=project_id, location=location)
            cls._vertex_ai_client = aiplatform
        return cls._vertex_ai_client

    @classmethod
    def get_vertex_ai_model_garden_client(cls):
        if cls._vertex_ai_model_garden_client is None:
            # The GenerativeModel client is initialized with a specific model ID
            # For safety, we'll use a text model that supports safety attributes.
            # The actual model ID might vary based on availability and specific safety features.
            # For embedding, we'll use a specific embedding model.
            # We'll initialize aiplatform.init once for all Vertex AI services.
            cls.get_vertex_ai_client()  # Ensure aiplatform is initialized
            from vertexai.preview.generative_models import GenerativeModel

            cls._vertex_ai_model_garden_client = GenerativeModel(
                "gemini-1.0-pro"
            )  # Using a general model for text processing and safety checks
        return cls._vertex_ai_model_garden_client

    @classmethod
    def get_vertex_ai_embedding_model(cls):
        cls.get_vertex_ai_client()  # Ensure aiplatform is initialized
        from vertexai.language_models import TextEmbeddingModel

        return TextEmbeddingModel.from_pretrained("text-embedding-004")
