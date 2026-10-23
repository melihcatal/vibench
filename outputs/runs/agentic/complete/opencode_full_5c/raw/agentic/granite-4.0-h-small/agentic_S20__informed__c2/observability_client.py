import os
import logging
from aliyun.log import LogClient

# Global client initialized with default credentials
LOG_CLIENT = None
_LOGGER = logging.getLogger(__name__)

# Datadog credentials for write_correlated_logs.py
_datadog_api_key = None
_datadog_app_key = None


def get_log_client():
    global LOG_CLIENT
    if not LOG_CLIENT:
        LOG_CLIENT = LogClient(
            endpoint=os.getenv("ALIBABA_CLOUD_LOG_ENDPOINT"),
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )
    return LOG_CLIENT


# Datadog log ingestion API client (requests.Session)
_ddog_session = None


def get_datadog_api_key():
    global _datadog_api_key
    if not _datadog_api_key:
        _datadog_api_key = os.getenv("DD_API_KEY")
    return _datadog_api_key


def get_datadog_app_key():
    global _datadog_app_key
    if not _datadog_app_key:
        _datadog_app_key = os.getenv("DD_APPLICATION_KEY")
    return _datadog_app_key


def init_datadog_session():
    global _ddog_session
    if not _ddog_session:
        _ddog_session = requests.Session()
        _ddog_session.headers.update(
            {
                "Content-Type": "application/json",
                "DD-API-KEY": get_datadog_api_key(),
                "DD-APPLICATION-KEY": get_datadog_app_key(),
            }
        )
    return _ddog_session


# Google Cloud Logging helper
_gcp_client = None


def get_gcp_client():
    global _gcp_client
    if not _gcp_client:
        # Ensure credentials are available via env var
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            _LOGGER.warning(
                "GOOGLE_APPLICATION_CREDENTIALS not set, using default credentials"
            )
        _gcp_client = gcp_logging.Client()
    return _gcp_client


# Utility to pull a generic environment‑based log field filter
FIELD_FILTER = os.getenv("LOG_FIELD_FILTER")  # e.g. 'severity=ERROR'


def get_field_filter():
    return FIELD_FILTER


# Correlation ID helpers (used in write_correlated_logs)
def generate_correlation_id():
    # Simple UUID‑v4 generator; in real️⃣ code you'd reuse an existing library
    import uuid

    return str(uuid.uuid4())


def get_correlation_id(request_id=None):
    if request_id:
        return request_id
    return generate_correlation_id()


# Logging configuration for all modules
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
)

# Simple logger for helper module itself
_LOGGER.info("observability_client.py loaded")
