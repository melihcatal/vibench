import boto3

def moderate_batch(messages):
    comprehend = boto3.client('comprehend')
    results = []
    for message in messages:
        result = comprehend.detect_sentiment(Text=message, LanguageCode='en')
        results.append(result['Sentiment'])
    return results

if __name__ == '__main__':
    messages = ['I love this product!', 'This is the worst service ever.']
    print(moderate_batch(messages))