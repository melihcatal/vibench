import logging
import os
import sys
import uuid

import requests


def _configure_logger() -> logging.Logger:
    logger = logging.getLogger("correlated_logs")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def _emit_log(logger: logging.Logger, provider: str, correlation_id: str, event: str, **fields) -> None:
    payload = {
        "provider": provider,
        "correlation_id": correlation_id,
        "event": event,
        **fields,
    }
    logger.info(payload)


def main() -> None:
    logger = _configure_logger()
    correlation_id = os.getenv("CORRELATION_ID", str(uuid.uuid4()))
    provider = "requests"

    _emit_log(logger, provider, correlation_id, "request_started", method="GET", url="https://httpbin.org/get")

    response = requests.get("https://httpbin.org/get", headers={"X-Correlation-ID": correlation_id}, timeout=10)

    _emit_log(
        logger,
        provider,
        correlation_id,
        "request_completed",
        status_code=response.status_code,
        response_bytes=len(response.content),
    )


if __name__ == "__main__":
    main()
