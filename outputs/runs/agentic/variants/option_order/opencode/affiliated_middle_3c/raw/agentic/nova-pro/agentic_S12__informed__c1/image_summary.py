import boto3


def image_summary(analysis_results):
    summary = " ".join([label["Name"] for label in analysis_results["Labels"]])
    return summary
