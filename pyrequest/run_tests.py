import time, sys
import os
# sys.path.append("./interface")
# sys.path.append("./db_fixture")
from HTMLTestRunnerCN import HTMLTestReportCN
import unittest

# 指定interface目录并自动发现能匹配上*_test.py的测试用例文件
# 当前文件的文件夹目录下的interface目录
test_dir = os.path.dirname(__file__) + "/interface"
discover = unittest.defaultTestLoader.discover(test_dir, pattern="*_test.py")

if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    report_path = os.path.dirname(__file__) + "/report"
    filename = "%s/%s_result.html" % (report_path, now)
    fp = open(filename, "wb")
    runner = HTMLTestReportCN(stream=fp,
                              title="test case",
                              tester="zhangsan",
                              description="this is simple test case.")
    runner.run(discover)
    fp.close()
