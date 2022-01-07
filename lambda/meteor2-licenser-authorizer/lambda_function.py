import os
import json
import models.mysql
import models.authorizer

def response(valid):
    return {
        "principalId": "meteor2-licenser",
        "policyDocument": { 
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Resource": "arn:aws:execute-api:eu-west-1:633757032102:1rry1aya5j/*/*",
                "Effect": "Allow" if valid else "Deny"
            }]
        }
    }

def lambda_handler(event, context):
    if 'authorizationToken' not in event:
        return response(False)
    try:
        sql = models.mysql.mysql()
        sql.connect(os.environ['HOSTNAME'], os.environ['USERNAME'], os.environ['PASSWORD'], int(os.environ['PORT']), os.environ['DATABASE'])
        authorizer = models.authorizer.Authorizer(sql)
        valid = authorizer.get(event['authorizationToken'])
        return response(valid)
    except Exception:
        return response(False)
    finally:
        sql.close()
