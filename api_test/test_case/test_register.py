import json
import unittest

from api_test.common.do_excel import DoExcel
from api_test.common import project_path
from api_test.common.http_request import HttpRequest
from api_test.common.my_log import MyLog
from ddt import ddt, data, unpack

# test_data = DoExcel(case_path, "register").read_case("CASE")
test_data = DoExcel(project_path.case_path, "register").read_case('RegisterCase')
my_log = MyLog()


@ddt
class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.t = DoExcel(project_path.case_path, 'register')  # 赋值给对象属性self.t,在整个类里面都可以调用，主要是写回操作用到
        print('開始執行新一條測試了')

    def tearDown(self) -> None:
        print('一條測試用例執行完畢')  # 清場工作，把占用的環境資源關掉

    @data(*test_data)
    def test_register(self, case):
        method = case['Method']
        url = case['Url']
        param = eval(case['Params'])  # 讀出來是個字符串，必須eval()變回原來字典類型
        my_log.info('-----正在测试{}模块里面第{}条测试用例：{},'.format(case['Module'], case['CaseId'], case['Title']))
        my_log.info('测试数据是：{}'.format(case['Params']))
        res = HttpRequest().http_request(method, url, param, cookies=None)
        try:
            # self.assertEqual(case["ExpectedResult"], res.text)
            self.assertEqual(json.loads(case["ExpectedResult"]), res.json())
            test_result = "Pass"
        except Exception as e:
            my_log.error("http请求出错了，错误是：{}".format(e))
            test_result = "Failed"
            raise e  # 抛出错误，否则测试报告那里全部都是通过
        finally:
            self.t.write_back(case['CaseId'] + 1, 9, res.text)  # 写回实际结果字符串类型不能用json，参数：行 列 实际结果
            self.t.write_back(case['CaseId'] + 1, 10, test_result)
        my_log.info('实际结果是:{}'.format(res.json()))

# param = eval(case['Params'])一直报错KeyError:'Parmas',原因是Excel中的Resgister模块的Params写成了Parmas,改回来之后还是错，原因是
# do_excel模块的Params也写成了Parmas
