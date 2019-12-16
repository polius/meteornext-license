class Licenses:
    def __init__(self, sql):
        self._sql = sql

    def get(self, email):
        query = """
            SELECT `email`, `key`, `expiration` 
            FROM `licenses`
            WHERE `email` = %s
        """
        return self._sql.execute(query, (email))
