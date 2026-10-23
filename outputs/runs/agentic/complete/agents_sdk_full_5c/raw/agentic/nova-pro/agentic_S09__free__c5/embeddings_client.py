import os
from cohere import Client

co = Client(os.getenv('COHERE_API_KEY'))
