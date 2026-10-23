import os
from typing import Optional

def get_project_id() -> Optional[str]:
    return os.getenv('GOOGLE_CLOUD_PROJECT')

def get_default_logger_name() -> str:
    return 'observability-logs'