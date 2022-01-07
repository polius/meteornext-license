class Authorizer:
    def __init__(self, sql):
        self._sql = sql

    def get(self, access_key):
        query = """
            SELECT EXISTS (
                SELECT *
                FROM licenses
                WHERE access_key = %s
            ) AS exist
        """
        return self._sql.execute(query, (access_key))[0]['exist']
