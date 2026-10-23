# describe_image.py
# [SAME-SCENARIO] Generate a short visual description for an image using Vision API

from vision_client import describe_image
from vision_models import normalize_caption

import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate a short caption for an image.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    args = parser.parse_args()

    raw_caption = describe_image(args.image_path)
    caption = normalize_caption(raw_caption)
    print('Image caption:', caption)

if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------------------------
# Note: Leverages Google Cloud Vision SDK (google-cloud-vision) with credentials from
# GOOGLE_APPLICATION_CREDENTIALS.
# ----------------------------------------------------------------------------------------------
