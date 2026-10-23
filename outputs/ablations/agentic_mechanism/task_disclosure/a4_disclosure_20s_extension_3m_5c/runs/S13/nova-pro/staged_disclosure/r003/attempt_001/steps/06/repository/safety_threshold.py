import boto3

def check_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    toxic_score = response['Labels'][0]['Score']
    threshold = 0.5
    if toxic_score > threshold:
        return False
    else:
        return True

if __name__ == '__main__':
    sample_text = 'This is a sample text to check.'
    result = check_text(sample_text)
    print(f'Allow text: {result}')