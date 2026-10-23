import boto3

def moderate_transcript(transcript_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': transcript_text
            }
        ],
        LanguageCode='en'
    )
    toxic_content = response['ToxicContent']
    if toxic_content:
        print('Toxic content detected: ', toxic_content)
        return False
    else:
        print('No toxic content detected.')
        return True

if __name__ == '__main__':
    sample_transcript = 'This is a sample transcript text.'
    if moderate_transcript(sample_transcript):
        print('Transcript is ready for publishing.')
    else:
        print('Transcript needs moderation before publishing.')