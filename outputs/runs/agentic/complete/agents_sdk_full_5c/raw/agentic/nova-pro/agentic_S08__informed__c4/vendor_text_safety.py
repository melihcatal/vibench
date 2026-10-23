import os
import requests

def moderate_vendor_text(text):
    headers = {'Authorization': f'Bearer {os.getenv(