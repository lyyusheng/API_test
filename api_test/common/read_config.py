from configparser import ConfigParser
from api_test.common import project_path


class ReadConfig:
    """此类用于读取配置文件"""

    def __init__(self, file_name):
        self.cf = ConfigParser()
        # 第一步：打开文件 调用read()方法，源码里面调用的是open的
        self.cf.read(file_name, encoding='utf-8')  # 内容有中文时要设置encoding

    def get_str(self, section, option):
        """获取字符串类型的"""
        value = self.cf.get(section, option)
        return value

    def get_boot(self, section, option):
        value = self.cf.getboolean(section, option)
        return value

    def get_float(self, section, option):
        value = self.cf.getfloat(section, option)
        return value

    def get_int(self, section, option):
        value = self.cf.getint(section, option)
        return value

    def get_data(self, section, option):
        value = self.cf.get(section, option)
        return eval(value)  # eval()可以把value转回原来的数据类型
        # 但是注意，有个玩死人的大坑，配置文件中列表元素如果混入了中文的逗号，就会报错！！！！！


if __name__ == '__main__':
    res = ReadConfig(project_path.conf_path).get_data('CASE', 'case_id')
    print(res)
    print(type(res))
