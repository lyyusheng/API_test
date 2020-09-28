import json
from api_test.common import do_excel
from api_test.common import project_path
from api_test.common import my_log
from api_test.common.http_request import HttpRequest
import unittest
from ddt import ddt, data
from api_test.common import get_data
from api_test.common.get_data import GetData
from api_test.common.do_pymysql import DoMysql

test_data = do_excel.DoExcel(project_path.case_path, "invest").read_case("InvestCase")
my_log = my_log.MyLog()


@ddt
class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.t = do_excel.DoExcel(project_path.case_path, "invest")

    def tearDown(self) -> None:
        pass

    @data(*test_data)
    def test_invest(self, case):
        method = case["Method"]
        url = case["Url"]
        param = eval(get_data.re_p(case["Params"]))

        if case["sql"] is not None:
            sql = eval(case["sql"])["sql"]
            before_amount = DoMysql().do_mysql(sql, 1)[0]
            invest_amount = int(param["amount"])

        res = HttpRequest().http_request(method, url, param, cookies=getattr(GetData, "COOKIES"))
        if res.cookies:
            setattr(GetData, "COOKIES", res.cookies)

        if case["sql"] is not None:
            sql = eval(case["sql"])["sql"]
            after_amount = DoMysql().do_mysql(sql, 1)[0]
            expect_amount = before_amount - invest_amount
            self.assertEqual(after_amount, expect_amount)

        try:
            self.assertEqual(json.loads(case["ExpectedResult"]), res.json())
            # self.assertEqual(eval(case["ExpectedResult"]), res.json())
            test_result = "Pass"
        except AssertionError as e:
            test_result = "Failed"
            my_log.error("http请求出错了，错误是{}".format(e))
            raise e
        finally:
            self.t.write_back(case["CaseId"] + 1, 9, res.text)
            self.t.write_back(case["CaseId"] + 1, 10, test_result)

# 报错json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
# 原因：json.loads() ，Excel的数据必须用双引号，不能用单引号
