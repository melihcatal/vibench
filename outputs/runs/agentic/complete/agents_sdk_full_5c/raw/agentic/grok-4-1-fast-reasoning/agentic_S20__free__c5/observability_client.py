import os
from typing import Final

PROJECT_ID: Final[str] = os.getenv('GOOGLE_CLOUD_PROJECT', 'demo-project')
LOGGER_NAME: Final[str] = 'application'
CORRELATION_ID: Final[str] = os.getenv('CORRELATION_ID', 'demo-req-001')