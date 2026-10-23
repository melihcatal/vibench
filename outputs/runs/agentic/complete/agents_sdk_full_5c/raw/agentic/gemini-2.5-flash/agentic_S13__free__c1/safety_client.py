import os
from google.cloud import aiplatform
from google.cloud import dlp_v2
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech_v1 as texttospeech

class SafetyClients:
    """
    Provides configured client instances for various Google Cloud APIs
    used in the text content safety task set.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SafetyClients, cls).__new__(cls)
            cls._instance._initialize_clients()
        return cls._instance

    def _initialize_clients(self):
        project_id = os.environ.get("GCP_PROJECT_ID")
        location = os.environ.get("GCP_LOCATION", "us-central1")

        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")

        # Initialize AI Platform for Generative Models and Embeddings
        aiplatform.init(project=project_id, location=location)
        self.generative_model_client = aiplatform.get_model("text-bison@001")
        self.embedding_model_client = aiplatform.get_model("text-embedding-gecko@001")

        # Initialize DLP Client
        self.dlp_client = dlp_v2.DlpServiceClient()

        # Initialize Translation Client
        self.translate_client = translate.Client(project=project_id)

        # Initialize Text-to-Speech Client
        self.tts_client = texttospeech.TextToSpeechClient()

    def get_generative_model_client(self):
        return self.generative_model_client

    def get_embedding_model_client(self):
        return self.embedding_model_client

    def get_dlp_client(self):
        return self.dlp_client

    def get_translate_client(self):
        return self.translate_client

    def get_tts_client(self):
        return self.tts_client

if __name__ == "__main__":
    # Example of how to use the client helper
    # Set GCP_PROJECT_ID and GCP_LOCATION environment variables for this to run.
    # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
    # os.environ["GCP_LOCATION"] = "us-central1"

    try:
        clients = SafetyClients()
        print("Clients initialized successfully.")

        gen_model = clients.get_generative_model_client()
        print(f"Generative Model: {gen_model.resource_name}")

        dlp_client = clients.get_dlp_client()
        print(f"DLP Client: {dlp_client}")

    except ValueError as e:
        print(f"Error initializing clients: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
