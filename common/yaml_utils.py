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


def replace_variables(data, variables):
    """
    递归替换数据结构中的 ${variable}占位符
    @:param data: 包含占位符的原始数据（可以是dict，list，str）
    @:param variable: 包含实际变量名和值的字典
    @:return: 动态替换后的数据
    """
    if isinstance(data, dict):
        return {k: replace_variables(v, variables) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_variables(i, variables) for i in data]
    elif isinstance(data, str):
        for var_name, var_value in variables.items():
            data = data.replace(f'${{{var_name}}}', str(var_value))
        return data
    else:
        return data
