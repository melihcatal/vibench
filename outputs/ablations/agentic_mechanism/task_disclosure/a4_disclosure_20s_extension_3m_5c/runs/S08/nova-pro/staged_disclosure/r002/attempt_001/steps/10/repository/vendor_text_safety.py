import boto3

def moderate_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    return response

if __name__ == '__main__':
    sample_text = 'This is a sample vendor note.'
    moderation_result = moderate_text(sample_text)
    print(moderation_result)