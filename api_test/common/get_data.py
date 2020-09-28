from api_test.common import read_config
from api_test.common import project_path
import re

config = read_config.ReadConfig(project_path.conf_path)


class GetData:
    COOKIES = None
    loan_id = None  # 新添加的标id初始值
    normal_usr = config.get_str('data', 'normal_usr')
    normal_pwd = config.get_str('data', 'normal_pwd')
    normal_member_id = config.get_str('data', 'normal_member_id')


def re_p(target):
    """通过正则表达式替换数据"""
    p = '#(.*?)#'  # 圆括号在正则表达式中代表组的意思,.表示通用匹配，*表示多次匹配,?表示找到一个就存一个，找过的不再找，原地开始找下一个

    while re.search(p, target):      # 正则表达式匹配到一次就进入循环替换一次， ?表示找到一个就存一个，找过的不再找，原地开始找下一个
        m = re.search(p, target)
        key = m.group(1)
        value = getattr(GetData, key)
        target = re.sub(p, value, target, count=1)
    return target
