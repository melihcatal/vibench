from transformers import pipeline

def check_unsafe_content(text):
    classifier = pipeline('text-classification', model='finiteautomata/bertweet-base-sentiment-analysis')
    result = classifier(text)
    return any(label['label'] == 'NEGATIVE' for label in result)