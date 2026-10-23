import boto3


def record_summary(document):
    summary = " ".join([v for k, v in document.items() if isinstance(v, str)])
    return summary[:200]
