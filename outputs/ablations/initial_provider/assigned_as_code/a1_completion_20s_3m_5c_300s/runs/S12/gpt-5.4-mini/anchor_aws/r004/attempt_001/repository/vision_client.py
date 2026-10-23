import os


def _env(name, default=None):
    value = os.getenv(name)
    return default if value in (None, "") else value


def get_provider_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or _env("AWS_REGION") or _env("AWS_DEFAULT_REGION"),
        "bucket": config.get("bucket") or _env("VISION_ARCHIVE_BUCKET"),
        "language": config.get("language") or _env("TARGET_LANGUAGE", "en"),
        "max_labels": int(config.get("max_labels", 10)),
        "translate_source_language": config.get("source_language") or _env("SOURCE_LANGUAGE", "auto"),
        "translate_target_language": config.get("target_language") or _env("TARGET_LANGUAGE", "es"),
    }


def rekognition_client(region=None):
    import boto3

    return boto3.client("rekognition", region_name=region)


def translate_client(region=None):
    import boto3

    return boto3.client("translate", region_name=region)


def s3_client(region=None):
    import boto3

    return boto3.client("s3", region_name=region)
