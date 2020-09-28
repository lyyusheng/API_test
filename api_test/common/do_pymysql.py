import pymysql
from api_test.common import read_config
from api_test.common import project_path


class DoMysql:
    """这个类用于操作数据库"""

    def do_mysql(self, query, flag):
        """
        query:sql查询语句
        flag:1表示获取第一条数据，2表示获取多条数据
        """
        # 获取数据库配置文件
        db_config = read_config.ReadConfig(project_path.conf_path).get_data('DB', 'db_config')
        # 链接数据库
        cnn = pymysql.connect(**db_config)
        # 建立游标
        cursor = cnn.cursor()
        # 执行SQL语句
        cursor.execute(query)
        if flag == 1:
            res = cursor.fetchone()
        else:
            res = cursor.fetchall()
        return res


if __name__ == '__main__':
    query = 'select * from member where MobilePhone=18300070752'
    res = DoMysql().do_mysql(query, 2)
    print('数据库的查询结果:{}'.format(res))
