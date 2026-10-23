# detect_image_text.py
# [SAME-SCENARIO] Extract text from an image using Vision API OCR

from vision_client import detect_text
from vision_models import normalize_ocr

import argparse

def main():
    parser = argparse.ArgumentParser(description='Perform OCR on an image and extract readable text.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    args = parser.parse_args()

    raw_texts = detect_text(args.image_path)
    texts = normalize_ocr(raw_texts)
    print('Extracted text:', texts)

if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------------------------
# Note: Uses Google Cloud Vision SDK (google-cloud-vision) and depends on
# GOOGLE_APPLICATION_CREDENTIALS for authentication.
# ----------------------------------------------------------------------------------------------
