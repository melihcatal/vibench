import argparse
import json
import os
from clarifai.client.model import Model
from vision_client import image_to_base64
from vision_models import ImageSafety

def score_image_safety(image_path: str) -> ImageSafety:
    pat = os.environ['CLARIFAI_PAT']
    model = Model("https://clarifai.com/clarifai/main/models/moderation-image", pat=pat)
    response = model.predict([{'base64': image_to_base64(image_path)}])
    concepts = response['outputs'][0]['data']['concepts']
    categories = {c['name']: c['value'] for c in concepts}
    return categories

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Score image safety using Clarifai')
    parser.add_argument('image_path', help='Path to input image')
    args = parser.parse_args()
    result = score_image_safety(args.image_path)
    print(json.dumps(result, indent=2))