import boto3

class SafetyThreshold:
    def __init__(self, comprehend_client):
        self.comprehend_client = comprehend_client

    def apply_thresholds(self, text, thresholds):
        response = self.comprehend_client.classify_document(
            Text=text,
           EndpointArn='arn:aws:comprehend:region:account-id:document-classifier/endpoint-name'
        )
        categories = response['Classes']
        decision = all(categories[category] <= threshold for category, threshold in thresholds.items())
        return decision

if __name__ == '__main__':
    comprehend_client = boto3.client('comprehend')
    safety_threshold = SafetyThreshold(comprehend_client)
    text_to_check = 'Sample text to check for safety.'
    thresholds = {'violence': 0.5, 'hate_speech': 0.3}
    decision = safety_threshold.apply_thresholds(text_to_check, thresholds)
    print('Text is safe:', decision)