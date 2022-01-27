"""Test serialise strategies."""
import pytest


@pytest.fixture
def datacache():
    """Setup/teardown fixture for datacache."""
    from oteapi.datacache import DataCache

    cache = DataCache()
    yield cache
    cache.evict(tag="test")


def test_serialise_json(datacache):
    """Test `text/json` serialise strategy."""
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.plugins import create_strategy

    data = {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }
    key = datacache.add(data, tag="test")

    config = ResourceConfig(
        downloadUrl="xxx://not.used/",  # not used, but required!
        mediaType="text/json",
        configuration={"accessKey": key},
    )
    serialiser = create_strategy("serialise", config)
    dct = serialiser.parse()
    value = dct["key"]
    print(value)

    assert value == data
