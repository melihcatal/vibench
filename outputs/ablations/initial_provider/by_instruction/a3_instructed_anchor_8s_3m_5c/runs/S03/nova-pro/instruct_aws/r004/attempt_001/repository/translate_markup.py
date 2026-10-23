import boto3
from bs4 import BeautifulSoup

def translate_markup(markup, source_language, target_language):
    client = boto3.client('translate')
    soup = BeautifulSoup(markup, 'html.parser')
    for tag in soup.find_all(text=True):
        if tag.parent.name not in ['style', 'script', '[document]', 'head', 'title']:
            translated_text = client.translate_text(Text=tag, SourceLanguageCode=source_language, TargetLanguageCode=target_language)['TranslatedText']
            tag.replace_with(translated_text)
    return str(soup)