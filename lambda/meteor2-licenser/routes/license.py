import uuid
import hashlib
from datetime import datetime
import models.licenses

class License:
    def __init__(self, event, context, sql):
        # Init models
        self._event = event
        self._context = context
        self._licenses = models.licenses.Licenses(sql)
        self.blueprint()

    def blueprint(self):
        # Get Request Json
        try:
            if 'access_key' not in self._event or 'secret_key' not in self._event or 'challenge' not in self._event:
                raise Exception()
        except Exception:
            return {
                'statusCode': 400,
                'body': {"response": "Invalid request", "date": str(datetime.utcnow())}
            }

        # Check Challenge Format
        try:
            uuid.UUID(self._event.get('challenge'), version=4)
        except ValueError:
            return {
                'statusCode': 401,
                'body': {"response": "Invalid request", "date": str(datetime.utcnow())}
            }

        # Get License
        license = self._licenses.get(self._event.get('access_key'))

        # Check if license exists
        if len(license) == 0:
            return {
                'statusCode': 401,
                'body': {"response": "Invalid credentials", "date": str(datetime.utcnow())}
            }
        license = license [0]

        # Check authentication
        if self._event.get('secret_key').encode('utf-8') != self._event.get('secret_key').encode('utf-8'):
            return {
                'statusCode': 401,
                'body': {"response": "The license is not valid", "date": str(datetime.utcnow())}
            }
        elif license['in_use'] and license['uuid'] != self._event.get('uuid'):
            return {
                'statusCode': 401,
                'body': {"response": "The license is already in use", "date": str(datetime.utcnow())}
            }
        else:
            self._licenses.post(self._event.get('access_key'), self._event.get('uuid'))
            return {
                'statusCode': 200,
                'body': {"response": "The license is valid", "challenge": self.__solve_challenge(self._event.get('challenge')), "date": str(datetime.utcnow()), "resources": license['resources'], "sentry": license['sentry']}
            }

    ####################
    # Internal Methods #
    #################### 
    def __solve_challenge(self, challenge):
        challenge2 = ','.join([str(ord(i)) for i in challenge])
        return hashlib.sha3_256(challenge2.encode()).hexdigest()