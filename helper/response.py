from flask import jsonify, make_response


def success_response(message, status):
    response = jsonify({'success': True, 'message': message, 'status': status})
    return make_response(response, status)


def error_response(message, status):
    response = jsonify({'success': False, 'error': message, 'status': status})
    return make_response(response, status)


def check_face_success(message, external_image_id, status, match):
    response = jsonify({'success': True, 'message': message,
                       'file': external_image_id, 'status': status, 'match': match})
    return make_response(response, status)


def check_face_error(message, external_image_id, status, match):
    response = jsonify({'success': False, 'message': message,
                       'file': external_image_id, 'status': status, 'match': match})
    return make_response(response, status)
