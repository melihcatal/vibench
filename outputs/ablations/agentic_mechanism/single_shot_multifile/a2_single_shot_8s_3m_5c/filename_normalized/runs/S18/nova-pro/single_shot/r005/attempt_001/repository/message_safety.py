from google.cloud import vision_v1

client = vision_v1.ImageAnnotatorClient()

image_path = 'path_to_your_image'
with open(image_path, 'rb') as image_file:
    image = vision_v1.Image(content=image_file.read())
response = client.safe_search_detection(image=image)
print(response.safe_search_annotation)