import boto3


def quality_summary(translated_segments, source_language, target_language):
    client = boto3.client("comprehend", region_name="us-east-1")
    issues = []
    for segment in translated_segments:
        language = client.detect_dominant_language(Text=segment)["Languages"][0]["LanguageCode"] if segment else target_language
        if language != target_language:
            issues.append({"segment": segment, "issue": "language_mismatch", "detected": language})
    return {"provider": "aws.comprehend", "source_language": source_language, "target_language": target_language, "issues": issues}
