import os

"""此模块用于读取文件路径"""
# project_path = os.path.realpath(--file--) 这里写错了
project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]  # 跟模块名一样，导入时注意别出错
# 测试用例路径
case_path = os.path.join(project_path, "test_case", "api_case_1.xlsx")

# 测试日志路径
log_path = os.path.join(project_path, "test_result", "test.log")

conf_path = os.path.join(project_path, "conf", "case.conf")
report_path = os.path.join(project_path, "test_result", "test_report.HTML")
