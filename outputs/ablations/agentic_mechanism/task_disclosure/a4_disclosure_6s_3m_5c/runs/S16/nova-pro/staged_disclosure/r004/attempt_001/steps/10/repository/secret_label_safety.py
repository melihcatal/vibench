import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

def main():
    secret_labels = ['label1', 'label2']
    secret_notes = ['note1', 'note2']
    for label in secret_labels:
        if check_unsafe_text(label):
            print(f'Unsafe text detected in label: {label}')
    for note in secret_notes:
        if check_unsafe_text(note):
            print(f'Unsafe text detected in note: {note}')

if __name__ == '__main__':
    main()