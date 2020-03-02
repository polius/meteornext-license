import uuid
import hashlib
from datetime import datetime
from flask import Blueprint, jsonify, request, redirect
import models.licenses

class License:
    def __init__(self, sql):
        # Init models
        self._licenses = models.licenses.Licenses(sql)

    def blueprint(self):
        # Init blueprint
        license_blueprint = Blueprint('license', __name__, template_folder='license')

        @license_blueprint.route('/', methods=['GET','POST'])
        def license_method():
            if request.method == 'GET':
                return redirect("https://meteor2.io", code=200)

            # Get Request Json
            params = request.get_json()

            # Check Params
            if 'email' not in params or 'key' not in params or 'challenge' not in params:
                return jsonify({"response": "The license is not valid"}), 401

            # Check Challenge Format
            try:
                uuid.UUID(params['challenge'], version=4)
            except ValueError:
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
            elif l[0]['in_use'] and l[0]['uuid'] != params['uuid']:
                return jsonify({"response": "The license is already in use"}), 401
            else:
                self._licenses.post(params['email'], params['uuid'])
                return jsonify({"response": "The license is valid", "challenge": self.__solve_challenge(params['challenge'])}), 200

        return license_blueprint

    ####################
    # Internal Methods #
    #################### 
    def __solve_challenge(self, challenge):
        challenge2 = ','.join([str(ord(i)) for i in challenge])
        return hashlib.sha3_256(challenge2.encode()).hexdigest()