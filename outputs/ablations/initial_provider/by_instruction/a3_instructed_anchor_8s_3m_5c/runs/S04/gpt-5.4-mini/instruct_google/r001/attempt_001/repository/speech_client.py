import os
from dataclasses import dataclass


@dataclass
class SpeechConfig:
    project_id: str
    location: str
    bucket_name: str
    google_application_credentials: str | None = None


def load_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us"),
        bucket_name=os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET", ""),
        google_application_credentials=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
    )


def parse_gs_uri(uri: str) -> tuple[str, str]:
    if not uri.startswith("gs://"):
        raise ValueError("expected gs:// uri")
    path = uri[5:]
    bucket, _, object_name = path.partition("/")
    if not bucket or not object_name:
        raise ValueError("invalid gs:// uri")
    return bucket, object_name


def default_output_uri(config: SpeechConfig, prefix: str) -> str:
    if not config.bucket_name:
        raise ValueError("GOOGLE_CLOUD_STORAGE_BUCKET is required")
    return f"gs://{config.bucket_name}/{prefix}"
