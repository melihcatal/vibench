import os


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "bucket": config.get("bucket") or os.getenv("VISION_ARCHIVE_BUCKET"),
        "language": config.get("language") or os.getenv("VISION_TARGET_LANGUAGE", "en"),
    }
