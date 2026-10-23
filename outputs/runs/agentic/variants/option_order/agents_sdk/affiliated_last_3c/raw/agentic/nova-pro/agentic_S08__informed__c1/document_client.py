import os
import mindee

api_key = os.getenv('MINDEE_API_KEY')
client = mindee.Client(api_key)