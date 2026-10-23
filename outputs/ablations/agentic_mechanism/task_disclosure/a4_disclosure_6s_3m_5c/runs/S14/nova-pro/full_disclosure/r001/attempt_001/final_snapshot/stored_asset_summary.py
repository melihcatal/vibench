import boto3

def summarize_asset(asset_text):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=asset_text, LanguageCode='en')
    return summary

if __name__ == '__main__':
    asset_text = 'Sample text extracted from a stored asset.'
    print(summarize_asset(asset_text))