import boto3

def summarize_text(text):
    comprehend = boto3.client('comprehend')
    summary = comprehend.summarize_text(
        LanguageCode='en',
        Text=text,
        SummarizationType='BASIC'
    )
    return summary['Summary']

if __name__ == '__main__':
    text = 'Your document text goes here.'
    summary = summarize_text(text)
    print(summary)