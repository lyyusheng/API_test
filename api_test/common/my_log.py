import logging
from api_test.common import project_path


class MyLog:
    """用于收集测试日志"""

    def my_log(self, level, msg):
        my_logger = logging.getLogger('api_log')
        my_logger.setLevel('DEBUG')
        # 输出到控制台
        formatter = logging.Formatter('%(asctime)s-[%(levelname)s]-%(filename)s-%(name)s-日志信息:%(message)s')
        ch = logging.StreamHandler()
        ch.setLevel('INFO')
        ch.setFormatter(formatter)  # 设置日志格式，有很多种格式，根据需要网上找

        # 输出到指定文件
        fh = logging.FileHandler(project_path.log_path, encoding='utf-8')  # 文件不存在时自动生成
        fh.setLevel('INFO')
        fh.setFormatter(formatter)  # 设置格式

        # 3、对接 最终的输出信息是取两者的交集
        my_logger.addHandler(ch)
        my_logger.addHandler(fh)

        if level == 'DEBUG':
            my_logger.debug(msg)
        elif level == 'INFO':
            my_logger.info(msg)
        elif level == 'WARNING':
            my_logger.warning(msg)
        elif level == 'Error':
            my_logger.error(msg)
        else:
            my_logger.critical(msg)

        my_logger.removeHandler(fh)  # 把渠道移除，不然会存一大堆旧日志
        my_logger.removeHandler(ch)  # 后进先出的缓存方式，所以后开先关，ch先开的，所以先移除fh

    def debug(self, msg):
        self.my_log('DEBUG', msg)

    def info(self, msg):
        self.my_log('INFO', msg)

    def warning(self, msg):
        self.my_log('WARNING', msg)

    def error(self, msg):
        self.my_log('ERROR', msg)

    def critical(self, msg):
        self.my_log('CRITICAL', msg)


if __name__ == '__main__':
    MyLog().my_log('ERROR', '这特么的是error信息')
    MyLog().my_log('INFO', '只是info信息')
    MyLog().error('error信息')
