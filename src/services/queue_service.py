import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

sqs = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

notification_queue_url = os.getenv("SQS_NOTIFICATION_QUEUE_URL")
listening_queue_url = os.getenv("SQS_LISTENING_QUEUE_URL")

def send_message(payload: dict):
    message_body = json.dumps(payload)
    response = sqs.send_message(
        QueueUrl=notification_queue_url,
        MessageBody=message_body
    )
    return response

def receive_messages():
    response = sqs.receive_message(
        QueueUrl=listening_queue_url,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=20
    )
    messages = response.get("Messages", [])
    if not messages:
        return None, None
    data = json.loads(messages[0]["Body"])
    return data, messages[0]["ReceiptHandle"]

def delete_message(receipt_handle: str):
    sqs.delete_message(
        QueueUrl=listening_queue_url,
        ReceiptHandle=receipt_handle
    )
