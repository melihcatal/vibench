# alt_text_translate.py
# [LATER-STEP] Translate the generated image caption into another language using the Google Cloud Translation API

from google.cloud import translate_v2 as translate
from pathlib import Path

# ----------------------------------------------------------------------------------------------
# Load the original caption from a text file produced by describe_image.py
# ----------------------------------------------------------------------------------------------
def load_caption(caption_path: Path, language: str = 'en') -> str:
    return caption_path.read_text(encoding='utf-8').strip()

# ----------------------------------------------------------------------------------------------
# Translate using Google Cloud Translation (v2 client; auth via GOOGLE_APPLICATION_CREDENTIALS)
# ----------------------------------------------------------------------------------------------
client = translate.Client()

def translate_caption(source_lang: str, target_lang: str, caption_path: Path) -> str:
    caption = load_caption(caption_path, source_lang)
    result = client.translate(caption, source_language=source_lang, target_language=target_lang)
    return result['translatedText']

# ----------------------------------------------------------------------------------------------
# Save translated text to a file
# ----------------------------------------------------------------------------------------------
def save_translation(translation: str, dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(translation, encoding='utf-8')

# ----------------------------------------------------------------------------------------------
# CLI entry point (uncomment to test)
# ----------------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     from argparse import ArgumentParser
#     parser = ArgumentParser(description='Translate an image caption.')
#     parser.add_argument('caption_path', type=str, help='Path to the original caption file.')
#     parser.add_argument('source_lang', type=str, help='Source language code, e.g., en.')
#     parser.add_argument('target_lang', type=str, help='Target language code, e.g., es.')
#     parser.add_argument('out_path', type=str, help='Path where translated caption will be saved.')
#     args = parser.parse_args()
#     translated = translate_caption(args.source_lang, args.target_lang, Path(args.caption_path))
#     save_translation(translated, Path(args.out_path))
#     print(f'Translation saved to {args.out_path}')

# ----------------------------------------------------------------------------------------------
# Note: This helper uses Google Cloud Translation SDK (google-cloud-translate) and
# relies on GOOGLE_APPLICATION_CREDENTIALS for authentication.
# ----------------------------------------------------------------------------------------------
