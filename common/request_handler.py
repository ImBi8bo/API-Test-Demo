"""处理HTTP请求"""

import requests


class RequestHandler:
    def __init__(self, base_url):
        """
        初始化 session和接口基地址
        :param base_url: 接口的基地址
        """
        self.session = requests.session()
        self.base_url = base_url
        self.variables = {}

    def request(self, method, url, **kwargs):
        """
        封装 HTTP请求方法
        :param method: 请求方法
        :param url: 请求url
        :param kwargs: 其他请求参数，如 params，headers，data，json等
        :return: 请求获取的 response对象
        """
        full_url = self.base_url + url
        resp = self.session.request(method, full_url, **kwargs)
        return resp
