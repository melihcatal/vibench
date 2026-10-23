from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient

class AzureObservabilityClient:
    def __init__(self):
        self._credential = DefaultAzureCredential()
        self.metrics_client = MetricsQueryClient(self._credential)

    def __enter__(self):
        return self.metrics_client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.metrics_client:
            self.metrics_client.close()


# Placeholder for GCP client if needed later
from google.cloud import storage, translate_v3, dlp_v2, aiplatform

class GcpObservabilityClient:
    def __init__(self):
        self.storage_client = storage.Client()
        self.translate_client = translate_v3.TranslationServiceClient()
        self.dlp_client = dlp_v2.DlpServiceClient()
        # Initialize Vertex AI client for summarization (using prediction service)
        # aiplatform.init() can be called once globally or for each client.
        # For this example, let's assume project and location are provided via config or environment.
        self.vertex_ai_client = aiplatform.gapic.PredictionServiceClient()

    # No __enter__ and __exit__ for GCP clients as they manage their own resources generally
