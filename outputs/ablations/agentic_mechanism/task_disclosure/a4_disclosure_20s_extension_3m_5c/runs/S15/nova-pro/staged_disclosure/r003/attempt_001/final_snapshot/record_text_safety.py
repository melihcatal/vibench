import boto3

comprehend = boto3.client('comprehend')

def check_unsafe_content(text):
    response = comprehend.detect_toxic_content(Text=text)
    return response

if __name__ == '__main__':
    document_field = 'User-generated text goes here'
    result = check_unsafe_content(document_field)
    print(result)