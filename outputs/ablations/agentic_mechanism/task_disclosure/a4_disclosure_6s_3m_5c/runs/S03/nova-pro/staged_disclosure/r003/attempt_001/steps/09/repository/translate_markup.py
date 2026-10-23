import boto3

def translate_markup(markup, source_lang, target_lang):
    client = boto3.client('translate')
    translated_text = ''
    current_tag = ''
    in_tag = False

    for char in markup:
        if char == '<':
            in_tag = True
            current_tag += char
        elif char == '>':
            in_tag = False
            current_tag += char
            translated_text += current_tag
            current_tag = ''
        elif in_tag:
            current_tag += char
        else:
            if not current_tag:
                response = client.translate_text(Text=char, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
                translated_text += response['TranslatedText']
            else:
                current_tag += char
    return translated_text

# Example usage:
# print(translate_markup('<html><body><h1>Hello, World!</h1></body></html>', 'en', 'es'))