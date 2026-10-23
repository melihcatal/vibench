import boto3
import io
from PIL import Image
import pytesseract
import spacy
from sentence_transformers import SentenceTransformer

def asset_metadata_embedding(bucket_name, object_key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([sent.text for sent in doc.sents])
    print(f'Embeddings: {embeddings}')
    return embeddings