import boto3

def apply_thresholds(text, thresholds):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    decision = {}
    for category, score in response['ToxicContentCategories'].items():
        if score > thresholds.get(category, 0):
            decision[category] = 'block'
        else:
            decision[category] = 'allow'
    return decision

if __name__ == '__main__':
    sample_text = 'Sample text to be moderated.'
    sample_thresholds = {'toxicity': 0.5, 'severe_toxicity': 0.2}
    decision = apply_thresholds(sample_text, sample_thresholds)
    print(decision)