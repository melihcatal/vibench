from observability_client import ObservabilityClient
from observability_models import StructuredLog


def write_structured_log(message: str, severity: str = "INFO", **kwargs):
    client = ObservabilityClient()
    logger = client.logging_client.logger(client.log_name)

    structured_log = StructuredLog(message, severity, **kwargs)
    logger.log_struct(structured_log.to_json(), severity=severity)
