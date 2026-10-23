from google.cloud import logging
from observability_client import get_google_cloud_project, get_default_logger_name
from observability_models import StructuredLogEvent

def write_structured_log(event: StructuredLogEvent, service: str = "general"):
    project = get_google_cloud_project()
    client = logging.Client(project=project)
    logger_name = get_default_logger_name(service)
    logger = client.logger(logger_name)
    logger.log_struct(event.to_dict())
