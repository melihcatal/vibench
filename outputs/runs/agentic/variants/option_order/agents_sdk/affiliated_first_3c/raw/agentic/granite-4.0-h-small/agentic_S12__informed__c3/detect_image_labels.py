# detect_image_labels.py
# [SAME-SCENARIO] Detect objects/labels in a static image using Vision API

from vision_client import detect_labels
from vision_models import normalize_labels

import argparse

def main():
    parser = argparse.ArgumentParser(description='Detect labels/objects in an image.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    args = parser.parse_args()

    raw = detect_labels(args.image_path)
    labels = normalize_labels(raw)
    print('Detected labels:', labels)

if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------------------------
# Note: This file uses Google Cloud Vision SDK (google-cloud-vision) and relies on the
# GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
# ----------------------------------------------------------------------------------------------
