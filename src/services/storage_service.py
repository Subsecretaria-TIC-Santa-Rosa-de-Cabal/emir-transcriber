import os
import tempfile

import boto3
from dotenv import load_dotenv


load_dotenv()

client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('S3_BUCKET_REGION'),
)
bucket_name = os.getenv('S3_BUCKET_NAME')
bucket_region = os.getenv('S3_BUCKET_REGION')

def get_local_file_path(remote_file_path: str) -> str:
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    client.download_file(bucket_name, remote_file_path, temp_path)
    return temp_path

def delete_local_file(local_file_path: str) -> None:
    if os.path.exists(local_file_path):
        os.remove(local_file_path)

def upload_text_remote_storage(text: str, file_path: str) -> None:
    client.put_object(
        Bucket=bucket_name,
        Key=file_path,
        Body=text,
        ContentType="text/plain"
    )
