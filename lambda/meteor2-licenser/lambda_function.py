import os
import json
import routes.license
import models.mysql
from datetime import datetime

def lambda_handler(event, context):
    # Instantiate SQL Class & Connect
    sql = models.mysql.mysql()
    try:
        sql.connect(os.environ['HOSTNAME'], os.environ['USERNAME'], os.environ['PASSWORD'], int(os.environ['PORT']), os.environ['DATABASE'])
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {"response": str(e), "date": str(datetime.utcnow())}
        }
    else:
        l = routes.license.License(event, context, sql)
        return l.blueprint()
    finally:
        sql.close()
