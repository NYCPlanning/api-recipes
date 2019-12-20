import os 
import boto3
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def make_client():
    session = boto3.session.Session()
    client = session.client('s3',
            region_name='S3_REGION',
            endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
            aws_access_key_id=os.environ.get('S3_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY'))
    return client

bucket = os.environ.get('S3_BUCKET')
