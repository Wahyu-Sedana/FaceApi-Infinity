from flask import Blueprint
from controller.face import *

face = Blueprint('api', __name__)

@face.route('/upload-face', methods=['POST'])
def uploadImageRoute():
    return uploadImage()

@face.route('/check-face', methods=['POST'])
def checkFaceRoute():
    return checkFace()