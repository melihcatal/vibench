import boto3

def moderate_messages(messages):
    comprehend = boto3.client('comprehend')
    results = []
    for message in messages:
        response = comprehend.detect_toxic_content(
            Text=message,
            LanguageCode='en'
        )
        results.append({
            'message': message,
            'decision': 'toxic' if response['ToxicContent'] else 'safe'
        })
    return results

if __name__ == '__main__':
    messages = [
        'This is a safe message.',
        'This message contains toxic content.'
    ]
    decisions = moderate_messages(messages)
    for decision in decisions:
        print(f"Message: {decision['message']}, Decision: {decision['decision']}")