import boto3

def check_platform_output_safety(text: str, threshold: float = 0.5) -> dict:
    client = boto3.client('comprehend', region_name='us-east-1')
    response = client.detect_toxicity(Text=text, LanguageCode='en')
    toxicity_score = response['Result']['Score']
    is_safe = toxicity_score < threshold
    return {
        'safe': is_safe,
        'toxicity_score': toxicity_score,
        'labels': response['Result'].get('Labels', [])
    }
