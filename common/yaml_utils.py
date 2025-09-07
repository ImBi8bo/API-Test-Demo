from pathlib import Path

import yaml

_cache = {}  # 将已经加载过的数据保存到字典实现缓存


def load_yaml_test_cases(yaml_file_name):
    """
    从 yaml文件加载测试用例
    :param yaml_file_name: yaml文件名，注意：要求测试用例放在 data目录下
    :return: yaml文件的数据
    """
    if yaml_file_name not in _cache:
        yaml_file_path = Path(__file__).resolve().parent.parent / 'data' / yaml_file_name
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            _cache[yaml_file_name] = yaml.safe_load(f)
    return _cache[yaml_file_name]
