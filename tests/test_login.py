# import jsonpath
import pytest

from common.yaml_utils import load_yaml_test_cases


class TestLogin:
    """测试登陆相关的api"""

    # 加载测试数据
    data = load_yaml_test_cases('login_test_data.yaml')

    def test_homepage(self, api_client):
        """测试首页接口，并提取 csrf_token"""

        hp_cases = TestLogin.data['homepage_cases'][0]  # 首页接口的测试用例
        # 发送请求
        resp = api_client.request(**hp_cases['request'])

        # 提取 csrf_token
        if 'extract' in hp_cases:
            api_client.extract_csrf_token(resp)

        # 断言响应结果
        assert resp.status_code == hp_cases['validate']['status_code']
        assert 'csrf_token' in resp.cookies

    @pytest.mark.parametrize('login_cases', data['login_cases'])
    def test_login(self, api_client, login_cases):
        """测试登录接口"""
        login_cases['request']['json']['csrf_token'] = api_client.variables['csrf_token']
        resp = api_client.request(**login_cases['request'])

        # 断言
        assert resp.status_code == login_cases['validate']['status_code']
        assert resp.json()['message'] == login_cases['validate']['message']
