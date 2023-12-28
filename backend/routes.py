from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item['id'] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({'error': 'Picture not found'}), 404
    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():

    # get data from the json body
    new_picture_data = request.get_json()
    print(new_picture_data)

    # Check if picture with the same ID already exists
     # if the id is already there, return 303 with the URL for the resource
    existing_picture = next((item for item in data if item['id'] == new_picture_data['id']), None)

    if existing_picture:
        return jsonify({'Message': f"picture with id {new_picture_data['id']} already present"}), 302
    else:
        data.append(new_picture_data)
        return jsonify({'id': new_picture_data['id']}), 201



######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture_data = request.get_json()

    # Find the picture in the data list
    picture_to_update = next((item for item in data if item['id'] == id), None)

    if picture_to_update:
        # Update the existing picture with the new data
        picture_to_update.update(updated_picture_data)
        return jsonify({'message': f'Picture with id {id} updated successfully'}), 200
    else:
        return jsonify({'message': 'Picture not found'}), 404





######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data  # Use 'global' to modify the global variable

    # Find the picture in the data list
    picture_to_delete = next((item for item in data if item['id'] == id), None)

    if picture_to_delete:
        # Delete the picture from the data list
        data = [item for item in data if item['id'] != id]
        return jsonify({}), 204  # No content (HTTP_204_NO_CONTENT)
    else:
        return jsonify({'message': 'Picture not found'}), 404
    
