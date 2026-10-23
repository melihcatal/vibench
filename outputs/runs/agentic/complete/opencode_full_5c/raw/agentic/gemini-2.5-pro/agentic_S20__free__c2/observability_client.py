import os
from google.cloud import logging
from google.cloud.logging_v2.services import logging_service_v2
from google.cloud import dlp_v2
from google.cloud import translate_v2 as translate
from google.cloud import aiplatform


def get_gcp_project_id():
    return os.environ.get("GCP_PROJECT_ID", "gcp-project-of-choice")


def get_logging_client() -> logging.Client:
    return logging.Client(project=get_gcp_project_id())


def get_logging_service_v2_client() -> logging_service_v2.LoggingServiceV2Client:
    return logging_service_v2.LoggingServiceV2Client()


def get_dlp_client() -> dlp_v2.DlpServiceClient:
    return dlp_v2.DlpServiceClient()


def get_translate_client() -> translate.Client:
    return translate.Client()


def initialize_vertex_ai():
    project_id = get_gcp_project_id()
    aiplatform.init(project=project_id, location="us-central1")
