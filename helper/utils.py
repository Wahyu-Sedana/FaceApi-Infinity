from config.credentials import *
import jwt
import os
from dotenv import load_dotenv
import base64

load_dotenv()


def verifyUser(file_stream):
    response = rekognition.search_faces_by_image(
        CollectionId= collection_id,
        FaceMatchThreshold= 95,
        Image={
            'Bytes': file_stream
        }
    )
    return response

def decryptJWT(token):
    secret_key = os.getenv("JWT_SECRET")

    token_bytes = token.encode('utf-8')
    base64ll = base64.b64decode(secret_key)
    
    try:
        payload = jwt.decode(token_bytes, key=base64ll, algorithms=["HS256"])
        # print('user_id_dec' + str(payload['sub']))
        return str(payload['sub'])
    except jwt.ExpiredSignatureError:
        return print("Token telah kedaluwarsa")
    except jwt.InvalidTokenError:
        return print("Token tidak valid")

def postImageOnCollection(file_stream, token):
    try:
        # print('token')
        # print(token)
        file_name = decryptJWT(token)
        # print('user_id_hel' + str(file_name))
        # Simpan gambar ke Amazon S3
        if file_name != False:
            s3_dest = s3_folder + file_name + '.jpeg' 
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
                ExternalImageId=file_name,
                QualityFilter="AUTO",
                MaxFaces=1,
                DetectionAttributes=['ALL']
            )
            return response
    except Exception as e:
        print(str(e))
        return None