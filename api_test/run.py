import os
from api_test.test_case import test_register, test_login, test_add_loan, test_recharge, test_invest
import unittest
import HTMLTestRunnerNew
from api_test.common import project_path
import sys
sys.path.append("./")



# 新建测试集
suite = unittest.TestSuite()
# 加载用例
loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_register))
suite.addTest(loader.loadTestsFromModule(test_register))
suite.addTest(loader.loadTestsFromModule(test_login))
suite.addTest(loader.loadTestsFromModule(test_add_loan))
suite.addTest(loader.loadTestsFromModule(test_recharge))
suite.addTest(loader.loadTestsFromModule(test_invest))
# 执行用例
with open(project_path.report_path, 'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              verbosity=2,
                                              title="2020年9月份api_test测试用例",
                                              description='总结时写的',
                                              tester='liyusheng')
    runner.run(suite)  # 执行用例（容易忘记,不写的话测试报告会空白.）

# TypeError: addTest() missing 1 required positional argument: 'test'
# 原因：suite = unittest.TestSuite()少写了（）
