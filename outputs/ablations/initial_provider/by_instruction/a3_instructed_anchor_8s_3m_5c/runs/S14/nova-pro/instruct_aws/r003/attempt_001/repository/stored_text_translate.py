import boto3
import io
from PIL import Image
import pytesseract
import translate

def stored_text_translate(bucket_name, object_key, target_language):
    text = stored_document_ocr(bucket_name, object_key)
    translator = translate.Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text