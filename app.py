from flask import Flask, request, jsonify
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
collection_id = os.getenv("COLLECTION_ID")
region = os.getenv("REGION")

s3_folder = os.getenv("S3_FOLDER")
s3_bucket = os.getenv("S3_BUCKET")

app = Flask(__name__)

rekognition = boto3.client('rekognition', 
                        region_name=region, 
                        aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key)
s3 = boto3.client('s3', 
                region_name=region, 
                aws_access_key_id=aws_access_key_id, 
                aws_secret_access_key=aws_secret_access_key)

def verifyUser(file_stream):
    response = rekognition.search_faces_by_image(
        CollectionId= collection_id,
        FaceMatchThreshold= 95,
        Image={
            'Bytes': file_stream
        }
    )
    return response

def postImageOnCollection(file_stream, external_image_id):
    response = rekognition.index_faces(
        CollectionId= collection_id,
        Image={
            'Bytes': file_stream
        },
        ExternalImageId= external_image_id,
        QualityFilter="AUTO",
        MaxFaces=3,
        DetectionAttributes=['ALL']
    )
    return response

def uploadToS3(file_stream, folder_name, file_name):
    response = s3.upload_fileobj(file_stream, s3_bucket, f"{folder_name}/{file_name}")
    return response


@app.route('/post', methods=['POST'])
def indexFace():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    try:
        external_image_id = file.filename
        external_image_id = external_image_id.split('.')[0] 
        face_records = postImageOnCollection(file.read(), external_image_id)
        if face_records:
            # Jika tidak ada wajah yang terdeteksi dengan ExternalImageId yang sama, maka upload gambar ke S3
            uploadToS3(file, s3_folder, file.filename)
            return jsonify({'result': 'Face indexed successfully', 'user_id': external_image_id})
        else:
            return jsonify({'error': 'No face detected in the image'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/check-face', methods=['POST'])
def checkFace():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        response = verifyUser(file.read())
        face_matches = response.get('FaceMatches', [])
        if face_matches:
            external_image_id = face_matches[0].get('Face', {}).get('ExternalImageId', 'Not available')
            return jsonify({'result': 'Face match found', 'user_id': external_image_id})
        else:
            return jsonify({'result': 'No face match found'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)