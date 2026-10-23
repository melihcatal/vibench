import boto3

def moderate_batch(messages):
    comprehend = boto3.client('comprehend')
    results = []
    for message in messages:
        response = comprehend.detect_toxic_content(
            Text=message,
            LanguageCode='en'
        )
        results.append(response['Labels'])
    return results

if __name__ == '__main__':
    messages = ['This is a nice message.', 'This is a toxic message.']
    print(moderate_batch(messages))