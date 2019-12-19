from datetime import datetime
from flask import Blueprint, jsonify, request
import models.licenses

class License:
    def __init__(self, sql):
        # Init models
        self._licenses = models.licenses.Licenses(sql)

    def blueprint(self):
        # Init blueprint
        license_blueprint = Blueprint('license', __name__, template_folder='license')

        @license_blueprint.route('/license', methods=['POST'])
        def license_method():
            # Get Request Json
            params = request.get_json()

            # Check Params
            if 'email' not in params and 'key' not in params:
                return jsonify({"response": "The license is not valid"}), 401

            # Get License
            try:
                l = self._licenses.get(params['email'])
            except Exception as e:
                return jsonify({"response": "Authentication failed. An error occurred during the authentication process"}), 401

            # Check authentication
            if len(l) == 0 or params['key'].encode('utf-8') != l[0]['key'].encode('utf-8'):
                return jsonify({"response": "The license is not valid"}), 401
            elif l[0]['expiration'] <= datetime.now():
                return jsonify({"response": "The license has expired"}), 401
            else:
                return jsonify({"response": "The license is valid"}), 200

        return license_blueprint
 