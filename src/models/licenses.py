class Licenses:
    def __init__(self, sql):
        self._sql = sql

    def get(self, email):
        query = """
            SELECT a.email, l.key, l.expiration, l.resources, l.in_use, l.uuid, l.last_used
            FROM licenses l
            JOIN accounts a ON a.id = l.account_id AND a.email = %s
        """
        return self._sql.execute(query, (email))

    def post(self, email, uuid):
        query = """
            UPDATE licenses
            JOIN accounts ON accounts.id = licenses.account_id
            SET licenses.in_use = 1,
                licenses.uuid = %s,
                licenses.last_used = CURRENT_TIMESTAMP
            WHERE accounts.email = %s
        """
        return self._sql.execute(query, (uuid, email))
