import os
from google.cloud import logging

client = logging.Client()
logger = client.logger("error_logs")
