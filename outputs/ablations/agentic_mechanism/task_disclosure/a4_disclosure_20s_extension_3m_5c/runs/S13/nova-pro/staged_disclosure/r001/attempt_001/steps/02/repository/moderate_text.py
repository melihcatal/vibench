import boto3

def score_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    return response

if __name__ == '__main__':
    user_text = input('Enter text to score: ')
    result = score_text(user_text)
    print(result)