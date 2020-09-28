import json

from api_test.common import do_excel
import unittest
from api_test.common import project_path
from api_test.common import my_log
from api_test.common.http_request import HttpRequest
from ddt import ddt, data

my_log = my_log.MyLog()

test_data = do_excel.DoExcel(project_path.case_path, "login").read_case("LoginCase")
print(test_data)


@ddt
class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.t = do_excel.DoExcel(project_path.case_path, "login")
        my_log.info("开始执行新一条测试用例")

    def tearDown(self) -> None:
        my_log.info("一条测试用例执行完毕")

    @data(*test_data)
    def test_login(self, case):
        method = case['Method']
        url = case['Url']
        param = eval(case['Params'])
        res = HttpRequest().http_request(method, url, param,cookies=None)
        try:
            # self.assertEqual(case["ExpectedResult"], res.json())
            # self.assertEqual(json.loads(case["ExpectedResult"]), res.json())    # 用了json.loads()包括Excel都不要用单引号，全部用双引号
            self.assertEqual(json.loads(case["ExpectedResult"]), res.json())
            test_result = "Pass"
        except Exception as e:
            my_log.error("http请求出错了，错误是：{}".format(e))
            test_result = "Failed"
            raise e  # 抛出错误，否则测试报告那里全部都是通过
        finally:
            self.t.write_back(case["CaseId"] + 1, 9, res.text)
            self.t.write_back(case["CaseId"] + 1, 10, test_result)
        my_log.info('实际结果是:{}'.format(res.json()))

# 出现Empty suite，一条用例都没有执行。原因是：函数名没有以test_开头，没识别出来

# 报错 json.decoder.JSONDecodeError: Expecting value: line 1 column 40 (char 39)。
# 原因：Excel中ExpectedResult的null写成None，如果双引号写成单引号也会
