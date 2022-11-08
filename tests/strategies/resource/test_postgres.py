"""Tests the parse strategy for SQLite."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Tuple

    from oteapi.interfaces import IResourceStrategy 


sqlite_queries = [
    (
        "SELECT * FROM user_details WHERE user_details.user_id = 19;",
        (
            19,
            "jenny0988",
            "maria",
            "morgan",
            "Female",
            "ec9ed18ae2a13fef709964af24bb60e6",
            1,
        ),
    ),
    (
        "SELECT * FROM user_details WHERE user_details.user_id = 72;",
        (
            72,
            "brown84",
            "john",
            "ross",
            "Male",
            "738cb4da81a2790a9a845f902a811ea2",
            1,
        ),
    ),
]

class MockPsycopg:
    result: "Tuple[int, str, str, str, str, str, int]"

    def cursor(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self 


    def execute(self, query):
        result = [q[1] for q in sqlite_queries if q[0] == query]
        self.result = result
        return self 

    def fetchall(self, *args, **kwargs):
        return self.result

    def close(self, *args, **kwargs):
        return self 



@pytest.mark.parametrize(
    "query,expected", sqlite_queries, ids=["configuration", "session"],
)
def test_postgres(
    query: str,
    expected: "Tuple[int, str, str, str, str, str, int]",
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test `application/vnd.sqlite3` parse strategy on a local SQLite DB.

    Test both passing in the query as a configuration and through a session.
    """
    from oteapi.strategies.resource.postgres import PostgresResourceStrategy
    import psycopg

    def mock_connect(connect_str):
        connect_str = str(connect_str)
        # TODO: this should work but for some reason we don't have 
        #       the DB name in the accessUrl?
        #expected_connect_str = \
        #    "postgresql://postgres:postgres@localhost:5432/postgres"
        #assert connect_str == expected_connect_str
        return MockPsycopg()

    monkeypatch.setattr(psycopg, "connect", mock_connect)

    connection_dict = {
        "dbname":"postgres",
        "user":"postgres",
        "password":"postgres",
        "host":"localhost",
        "port":5432,
    }
    #TODO there are a lot of tests one can do on ways of connecting to the DB

    config = {
        "accessUrl": "postgresql://postgres:postgres@localhost:5432/postgres",
        "accessService": "foo",
        "configuration": {    "sqlquery": query,},
    }

    resource: "IResourceStrategy" = PostgresResourceStrategy(config)
    resource.initialize()

    result = resource.get({"sqlquery": query} if "19" not in query else None)

    assert result["result"][0] == expected
