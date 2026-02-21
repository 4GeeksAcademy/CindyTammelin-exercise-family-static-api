"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    
    member = jackson_family.get_member(member_id)
    
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify(member), 200


@app.route('/members', methods=['POST'])
def add_member():
    
    member_data = request.get_json()
    
    
    if not member_data:
        return jsonify({"error": "No data provided"}), 400
    
    if "first_name" not in member_data:
        return jsonify({"error": "first_name is required"}), 400
    
    if "age" not in member_data:
        return jsonify({"error": "age is required"}), 400
    
    if "lucky_numbers" not in member_data:
        return jsonify({"error": "lucky_numbers is required"}), 400
    
   
    new_member = jackson_family.add_member(member_data)
    
    return jsonify(new_member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
   
    deleted_member = jackson_family.delete_member(member_id)
    
    if deleted_member is None:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"done": True}), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
