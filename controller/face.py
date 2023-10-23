from helper.response import *
from flask import request
from helper.utils import *
from config.database import mysql
from dotenv import load_dotenv
import os
load_dotenv()


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
            s3_url = os.getenv("S3_URL")
            usr_id = response["FaceRecords"][0]["Face"]["ExternalImageId"]
            img_url = s3_url+usr_id+'.jpeg'
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE users SET face_id = %s WHERE id = %s", (img_url, usr_id))
            mysql.connection.commit()
            return success_response("Face ID success uploaded", status=200)
        else:
            return error_response("Failed to upload Face ID", status=500)
    except Exception as e:
        return error_response(str(e), status=500)


def checkFace():
    if 'file' not in request.files and 'sesi' not in request.form:
        return error_response('No file part', status=400)

    file = request.files['file']
    sesi = request.form['sesi']

    if file.filename == '':
        return error_response('No selected file', status=400)

    try:
        response = verifyUser(file.read())
        face_matches = response.get('FaceMatches', [])
        if face_matches:
            external_image_id = face_matches[0].get(
                'Face', {}).get('ExternalImageId', 'Not available')
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT registrations.id FROM registrations INNER JOIN transactions ON registrations.transaction_id = transactions.id INNER JOIN events ON registrations.event_id = events.id WHERE events.type = 'seminar' AND event_level_id = 5 AND registrations.user_id = %s AND transactions.status = 'paid'", (external_image_id,))
            reg_id = cur.fetchone()
            print(reg_id[0])
            if reg_id:
                if sesi == '1':
                    response1 = cur.execute(
                        "UPDATE registrations SET attendance = 1, check_first = CURRENT_TIMESTAMP WHERE id = %s", (reg_id[0],))
                    print(response1)
                    mysql.connection.commit()
                elif sesi == '2':
                    response2 = cur.execute(
                        "UPDATE registrations SET check_second = CURRENT_TIMESTAMP WHERE id = %s", (reg_id[0],))
                    print(response2)
                    mysql.connection.commit()
            cur.close()
            return check_face_success('Face match found', status=200, external_image_id=external_image_id, match=True)
        else:
            return check_face_success('No face match found', status=200, external_image_id='Not available', match=False)
    except Exception as e:
        return error_response(str(e), status=500)
