import os
from google.cloud import vision

def check_image_safety(image_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}".format(response.error.message))

    print("Safe search results:")
    print(
        "Adult: {}".format(response.safe_search_annotation.adult))
    print(
        "Spoof: {}".format(response.safe_search_annotation.spoof))
    print(
        "Medical: {}".format(response.safe_search_annotation.medical))
    print(
        "Violence: {}".format(response.safe_search_annotation.violence))

    if (response.safe_search_annotation.adult == vision.Likelihood.LIKELY or
        response.safe_search_annotation.spoof == vision.Likelihood.LIKELY or
        response.safe_search_annotation.medical == vision.Likelihood.LIKELY or
        response.safe_search_annotation.violence == vision.Likelihood.LIKELY):
        print("Image contains unsafe content.")
    else:
        print("Image is safe.")

if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    check_image_safety(image_path)