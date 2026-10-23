import boto3
from safety_models import ModerationInput, ThresholdDecision

# Define custom thresholds for flagging content from AWS Comprehend
THRESHOLDS = {
    "TOXICITY": 0.75,
    "PROFANITY": 0.8,
    "HATE_SPEECH": 0.6,
    "INSULT": 0.7,
}

def apply_safety_thresholds(input_data: ModerationInput) -> ThresholdDecision:
    """
    Applies custom category thresholds to decide whether to allow text
    using AWS Comprehend for toxicity analysis.
    """
    # boto3 will use credentials from environment variables (e.g. AWS_ACCESS_KEY_ID) or IAM roles
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

    response = comprehend.detect_toxic_content(
        TextSegments=[{'Text': input_data.text}],
        LanguageCode='en'
    )

    result = response['ResultList'][0]
    violated_categories = []
    is_safe = True

    # Check the overall toxicity score
    if result['Toxicity'] >= THRESHOLDS['TOXICITY']:
        is_safe = False
        violated_categories.append("TOXICITY")

    # Check individual label scores
    for label in result['Labels']:
        if label['Name'] in THRESHOLDS and label['Score'] >= THRESHOLDS[label['Name']]:
            is_safe = False
            if label['Name'] not in violated_categories:
                violated_categories.append(label['Name'])

    return ThresholdDecision(
        text=input_data.text,
        is_safe=is_safe,
        violated_categories=list(set(violated_categories))
    )
