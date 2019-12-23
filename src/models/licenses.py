class Licenses:
    def __init__(self, sql):
        self._sql = sql

    def get(self, email):
        query = """
            SELECT `email`, `key`, `expiration`, `in_use`, `uuid`, `last_used`
            FROM `licenses`
            WHERE `email` = %s
        """
        return self._sql.execute(query, (email))

    def post(self, email, uuid):
        query = """
            UPDATE `licenses`
            SET `in_use` = 1,
                `uuid` = %s,
                `last_used` = CURRENT_TIMESTAMP
            WHERE `email` = %s 
        """
        return self._sql.execute(query, (uuid, email))
