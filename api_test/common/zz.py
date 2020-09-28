import re

from api_test.common import read_config
from api_test.common import project_path
import re

config = read_config.ReadConfig(project_path.conf_path)


class GetData:
    COOKIES = None
    LOAN_ID = None  # 新添加的标id初始值
    normal_usr = config.get_str('data', 'normal_usr')
    normal_pwd = config.get_str('data', 'normal_pwd')
    normal_member_id = config.get_str('data', 'normal_member_id')


def re_p(target):
    p = '#(.*?)#'
    while re.search(p, target):
        m = re.search(p, target)
        key = m.group(1)
        value = getattr(GetData, key)
        target = re.sub(p, value, target, count=1)
    print(target)


if __name__ == '__main__':
    target = '{"mobilephone":"#normal_usr#","pwd":"#normal_pwd#"}'
    re_p(target)
