import boto3

def check_annotation_safety(
    text: str,
    language_code: str = 'en',
    toxicity_threshold: float = 0.5
) -> Dict[str, bool]:
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(
        Text=text,
        LanguageCode=language_code
    )
    results = {}
    for item in response['ResultList']:
        name = item['Name']
        score = item['Score']
        results[name] = score > toxicity_threshold
    return results
