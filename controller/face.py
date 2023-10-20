from helper.response import *
from flask import request
from helper.utils import *

def uploadImage():
    if 'file' not in request.files or 'token' not in request.form:
        return error_response('No file or token provided', status=400)

    file = request.files['file']
    token = request.form['token']

    if file.filename == '':
        return error_response('No selected file', status=400)

    if token is None:
        return error_response('Invalid or expired token', status=401)

    try:
        file_stream = file.read()
        response = postImageOnCollection(file_stream, token)
        if response:
            return success_response("Image uploaded to S3 and added to Rekognition collection", status=200)
        else:
            return error_response("Failed to upload to S3 or add to Rekognition collection", status=500)
    except Exception as e:
        return error_response(str(e), status=500)

    
def checkFace():
    if 'file' not in request.files:
        return error_response('No file part', status=400)

    file = request.files['file']

    if file.filename == '':
        return error_response('No selected file', status=400)

    try:
        response = verifyUser(file.read())
        face_matches = response.get('FaceMatches', [])
        if face_matches:
            external_image_id = face_matches[0].get('Face', {}).get('ExternalImageId', 'Not available')
            return check_face_success('Face match found', status=200, external_image_id=external_image_id, match=True)
        else:
            return check_face_success('No face match found', status=200, external_image_id='Not available', match=False)
    except Exception as e:
        return error_response(str(e), status=500)