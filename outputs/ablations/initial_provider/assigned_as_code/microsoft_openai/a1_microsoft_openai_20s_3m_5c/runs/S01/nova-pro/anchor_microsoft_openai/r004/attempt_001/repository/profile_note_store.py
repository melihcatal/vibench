import boto3
from pymongo import MongoClient

def store_profile_note(user_id, note):
    client = MongoClient(boto3.client('docdb').describe_db_clusters()['DBClusters'][0]['Endpoint'])['onboarding_notes']
    client['notes'].update_one({'user_id': user_id}, {'$set': {'note': note}}, upsert=True)