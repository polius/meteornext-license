from datetime import datetime

class Licenses:
    def __init__(self, sql):
        self._sql = sql

    def get(self, access_key):
        query = """
            SELECT l.access_key, l.secret_key, p.resources, l.in_use, l.uuid, l.last_used, s.sentry_enabled AS 'sentry'
            FROM licenses l
            JOIN products p ON p.id = l.product_id
            LEFT JOIN accounts_sentry s ON s.account_id = l.account_id
            WHERE l.access_key = %s
        """
        return self._sql.execute(query, (access_key))

    def post(self, access_key, uuid):
        query = """
            UPDATE `licenses`
            SET `in_use` = 1,
                `uuid` = %s,
                `last_used` = %s
            WHERE `access_key` = %s
        """
        return self._sql.execute(query, (uuid, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), access_key))
