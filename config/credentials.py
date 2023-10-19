from dotenv import load_dotenv
import os
import boto3

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
collection_id = os.getenv("COLLECTION_ID")
region = os.getenv("REGION")

s3_folder = os.getenv("S3_FOLDER")
s3_bucket = os.getenv("S3_BUCKET")

rekognition = boto3.client('rekognition', 
                        region_name=region, 
                        aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key)
s3 = boto3.client('s3', 
                region_name=region, 
                aws_access_key_id=aws_access_key_id, 
                aws_secret_access_key=aws_secret_access_key)