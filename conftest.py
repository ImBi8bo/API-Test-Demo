import pytest

from common.request_handler import RequestHandler


@pytest.fixture(scope='session')
def api_client():
    """初始化测试环境"""
    base_url = 'https://m1.apifoxmock.com/m1/7035626-6755555-default/phpwind'
    client = RequestHandler(base_url)
    yield client
    client.session.close()
