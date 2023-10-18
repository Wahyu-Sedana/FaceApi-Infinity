from flask import jsonify, make_response

def success_response(message, status):
    response = jsonify({'success': True, 'message': message, 'status': status})
    return make_response(response, status)

def error_response(message, status):
    response = jsonify({'success': False, 'error': message, 'status': status})
    return make_response(response, status)

def check_face_success(message, external_image_id, status):
    response = jsonify({'success': True, 'message': message, 'user_id': external_image_id, 'status': status})
    return make_response(response, status)


def check_face_error(message, external_image_id, status):
    response = jsonify({'success': False, 'message': message, 'user_id': external_image_id, 'status': status})
    return make_response(response, status)