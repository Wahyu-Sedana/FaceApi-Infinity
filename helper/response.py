from flask import jsonify, make_response


def success_response(message, status):
    response = jsonify({'success': True, 'message': message, 'status': status})
    return make_response(response, status)


def error_response(message, status):
    response = jsonify({'success': False, 'error': message, 'status': status})
    return make_response(response, status)


def check_face_success(message, name, status, match):
    response = jsonify({'success': True, 'message': message,
                       'name': name, 'status': status, 'match': match})
    return make_response(response, status)


def check_face_error(message, status, match):
    response = jsonify({'success': False, 'message': message,
                        'status': status, 'match': match})
    return make_response(response, status)
