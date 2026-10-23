from observability_client import ObservabilityClient
from observability_models import CorrelatedLog


def write_correlated_logs(
    correlation_id: str, messages: list[str], severity: str = "INFO", **kwargs
):
    client = ObservabilityClient()
    logger = client.logging_client.logger(client.log_name)

    for message in messages:
        correlated_log = CorrelatedLog(correlation_id, message, severity, **kwargs)
        logger.log_struct(correlated_log.to_json(), severity=severity)
