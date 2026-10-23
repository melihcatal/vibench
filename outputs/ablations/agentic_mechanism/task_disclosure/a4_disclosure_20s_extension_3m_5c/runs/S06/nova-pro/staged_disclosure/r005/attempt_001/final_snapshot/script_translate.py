import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

def main():
    input_file = 'narration_script.txt'
    output_file = 'translated_script.txt'
    source_language = 'en'
    target_language = 'es'

    with open(input_file, 'r') as f:
        narration_script = f.read()

    translated_script = translate_text(narration_script, source_language, target_language)

    with open(output_file, 'w') as f:
        f.write(translated_script)

    print(f'Translated script written to {output_file}')

if __name__ == '__main__':
    main()