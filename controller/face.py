from app import rekognition, s3
from config.credentials import *

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