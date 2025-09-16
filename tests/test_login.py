import allure
import pytest

from common.yaml_utils import load_yaml_test_cases, replace_variables

# 加载测试数据
test_data = load_yaml_test_cases('login_test_data.yaml')

@allure.epic('TPshop')
@allure.feature('用户认证')
class TestLogin:
    """测试登陆相关的 api"""
    @allure.story('获取csrf_token')
    @allure.title('访问首页获取csrf_token')
    @pytest.mark.parametrize(
        "case_info",
        test_data['homepage_cases'],
        ids=[f"{case['test_id']}_{case['title']}" for case in test_data['homepage_cases']]
    )
    def test_homepage(self, api_client, case_info):
        """测试首页接口"""

        # 发送请求
        resp = api_client.request(**case_info['request'])

        # 断言响应结果
        assert resp.status_code == case_info['validate']['status_code']
        assert case_info['validate']['check_cookie'] in resp.cookies

    @allure.story('用户登录')
    @pytest.mark.parametrize(
        "case_info",
        test_data['login_cases'],
        ids=[f"{case['test_id']}_{case['title']}" for case in test_data['login_cases']]
    )
    def test_login(self, api_client, csrf_token, case_info):
        """测试登录接口"""

        # 1. 定义变量字典，保存实际替换的变量名和值
        variables = {
            'csrf_token': csrf_token
        }

        # 2. 动态替换请求数据中的占位符
        request_data = replace_variables(case_info['request'], variables)

        # 3. 发送请求
        resp = api_client.request(**request_data)

        # 4. 断言
        assert resp.status_code == case_info['validate']['status_code']
        if 'check_json' in case_info['validate']:
            for key, expected_value in case_info['validate']['check_json'].items():
                assert resp.json()[key] == expected_value
