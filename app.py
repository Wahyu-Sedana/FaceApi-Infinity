from flask import Flask, request, jsonify
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
collection_id = os.getenv("COLLECTION_ID")
region = os.getenv("REGION")

print(aws_access_key_id, aws_secret_access_key, region, collection_id)

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
    try:
        # Simpan gambar ke Amazon S3
        s3_dest = s3_folder + external_image_id + '.jpeg' 
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_dest,
            Body=file_stream,
            ACL='public-read',
            ContentType='image/jpeg'
        )

        # Tambahkan gambar ke koleksi Rekognition
        response = rekognition.index_faces(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_dest
                }
            },
            ExternalImageId=external_image_id,
            QualityFilter="AUTO",
            MaxFaces=1,
            DetectionAttributes=['ALL']
        )
        return response
    except Exception as e:
        print(str(e))
        return None

@app.route('/upload', methods=['POST'])
def uploadImage():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        file_stream = file.read()
        external_image_id = file.filename.split('.')[0]

        response = postImageOnCollection(file_stream, external_image_id)

        if response is not None:
            return jsonify({'result': 'Image uploaded to S3 and added to Rekognition collection'})
        else:
            return jsonify({'error': 'Failed to upload to S3 or add to Rekognition collection'})

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
    app.run(debug=True, port=5000)