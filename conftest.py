import pytest

from common.request_handler import RequestHandler
from common.yaml_utils import load_yaml_test_cases


@pytest.fixture(scope='session')
def api_client():
    """初始化测试环境"""
    base_url = 'https://m1.apifoxmock.com/m1/7035626-6755555-default/phpwind'
    client = RequestHandler(base_url)
    yield client
    client.session.close()


@pytest.fixture(scope='session')
def csrf_token(api_client):
    """提取 csrf_token"""

    # 加载对应的测试用例
    homepage_cases = load_yaml_test_cases('login_test_data.yaml').get('homepage_cases')[0]

    # 发送请求
    resp = api_client.request(**homepage_cases.get('request'))
    # print(resp.cookies.get('csrf_token'))

    # 添加简单的断言，保证前置步骤成功
    assert resp.status_code == homepage_cases['validate']['status_code']

    # 从 yaml测试用例获取提取规则
    token = None
    extract_rule = homepage_cases['extract']['csrf_token']

    # 这是一个简化的提取器
    if extract_rule == 'cookies.csrf_token':
        token = resp.cookies.get('csrf_token')

    if not token:
        print('无法提取到csrf_token')

    return token

# 解决ids参数在控制台不正常显示的问题
def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的用例名name和用例标识nodeid的中文信息正常显示在控制台上
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")