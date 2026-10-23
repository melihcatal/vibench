import boto3


def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response


if __name__ == '__main__':
    annotation = 'Example annotation with potentially unsafe content'
    result = check_unsafe_text(annotation)
    print(result)