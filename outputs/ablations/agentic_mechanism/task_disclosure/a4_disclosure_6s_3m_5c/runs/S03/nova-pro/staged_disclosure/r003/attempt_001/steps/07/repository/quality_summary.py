import boto3

def summarize_translation_quality():
    translate = boto3.client('translate', region_name='us-west-2')
    response = translate.get_terminology(
        Name='example-terminology'
    )
    quality_issues = response['TerminologyData']['File']['S3Uri']
    print(f'Translation quality issues: {quality_issues}')

if __name__ == '__main__':
    summarize_translation_quality()