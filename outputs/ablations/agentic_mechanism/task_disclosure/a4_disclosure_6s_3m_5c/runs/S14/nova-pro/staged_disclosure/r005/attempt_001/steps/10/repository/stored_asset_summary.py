import boto3

def summarize_asset(asset_content):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=asset_content, LanguageCode='en')
    return summary

if __name__ == '__main__':
    asset_content = 'Sample content extracted from a stored asset.'
    summary = summarize_asset(asset_content)
    print(summary)