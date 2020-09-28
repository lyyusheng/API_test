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

test_data = do_excel.DoExcel(project_path.case_path, "add_loan").read_case("AddLoanCASE")
my_log = my_log.MyLog()


@ddt
class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.t = do_excel.DoExcel(project_path.case_path, "add_loan")

    def tearDown(self) -> None:
        pass

    @data(*test_data)
    def test_add_loan(self, case):
        method = case["Method"]
        url = case["Url"]
        param = eval(get_data.re_p(case["Params"]))
        print(param)
        my_log.info('-------正在测试{}模块里面第{}条测试用例：{}'.format(case['Module'], case['CaseId'], case['Title']))
        my_log.info('测试数据是：{}'.format(case))

        res = HttpRequest().http_request(method, url, param, cookies=getattr(GetData, "COOKIES"))

        if case["sql"] is not None:
            loan_id = DoMysql().do_mysql(eval(case["sql"])["sql"], 1)
            setattr(GetData, "loan_id", str(loan_id[0]))  # loanid与Excel中的保持一致。从数据库查到的loan_id是int， 因为要用到正则表达式替换，所以改成str
            # 但是为啥这里是loan_id，而gte_data.py里面的是LOANID也可以？ excel、这里、还有get_data.py保持一致，似乎不分大小写

        if res.cookies:
            setattr(GetData, "COOKIES", res.cookies)

        try:
            self.assertEqual(json.loads(case["ExpectedResult"]), res.json())
            test_result = "Pass"
        # except Exception as e:
        except AssertionError as e:
            test_result = "Faild"
            my_log.error("http请求出错了，错误是{}".format(e))
            raise e
        finally:
            self.t.write_back(case["CaseId"] + 1, 9, res.text)
            self.t.write_back(case["CaseId"] + 1, 10, test_result)
        my_log.info('实际结果：{}'.format(res.json()))  # http发送请求拿到的实际返回值
# 报错：TypeError: decoding to str: need a bytes-like object, NoneType found
# 原因：setattr(GetData, "loan_id", str(loan_id[0]))
# 从数据库查到的loan_id是int， 因为要用到正则表达式替换，所以改成str
