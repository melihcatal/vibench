# score_image_safety.py
# [SAME-SCENARIO] Check an image for unsafe or policy-sensitive visual content (adult, violence, etc.)

from vision_client import score_safety
from vision_models import normalize_safety

import argparse

def main():
    parser = argparse.ArgumentParser(description='Evaluate safety flags on an image using Vision API.')
    parser.add_argument('image_path', type=str, help='Path to the image to analyze.')
    args = parser.parse_args()

    raw_flags = score_safety(args.image_path)
    safety_report = normalize_safety(raw_flags)
    print('Safety evaluation:', safety_report)

if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------------------------
# Note: Relies on Google Cloud Vision SDK (google-cloud-vision) and environment auth via
# GOOGLE_APPLICATION_CREDENTIALS.
# ----------------------------------------------------------------------------------------------
