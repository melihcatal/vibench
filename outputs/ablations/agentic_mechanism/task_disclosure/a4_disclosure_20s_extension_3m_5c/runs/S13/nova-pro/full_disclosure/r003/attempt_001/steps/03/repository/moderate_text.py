import boto3

def score_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    return response

if __name__ == '__main__'):
    text = 'Sample text to be scored for unsafe content.'
    result = score_text(text)
    print(result)