import os
from google.cloud import vision

def score_image_safety(image_path):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.
    """
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    print(f"Safe search results for {image_path}:")
    print(f"Adult: {vision.Likelihood(safe_search_annotation.adult).name}")
    print(f"Medical: {vision.Likelihood(safe_search_annotation.medical).name}")
    print(f"Spoof: {vision.Likelihood(safe_search_annotation.spoof).name}")
    print(f"Violence: {vision.Likelihood(safe_search_annotation.violence).name}")
    print(f"Racy: {vision.Likelihood(safe_search_annotation.racy).name}")

    return safe_search_annotation

if __name__ == '__main__':
    # For demonstration purposes, you would replace 'your_image.jpg' with an actual image path
    # and ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # For example:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # python score_image_safety.py your_image.jpg
    
    # You can provide an image path as a command-line argument or modify this directly
    if len(os.sys.argv) > 1:
        image_file_path = os.sys.argv[1]
    else:
        print("Please provide an image path as an argument. Example: python score_image_safety.py your_image.jpg")
        os.sys.exit(1)

    score_image_safety(image_file_path)
