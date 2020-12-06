import requests
import unittest


class GetEventListTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    # 发布会id为空
    def test_get_event_null(self):
        r = requests.get(self.url, params={"eid": ""})
        result = r.json()
        self.assertEqual(result["status"], 10021)
        self.assertEqual(result["msg"], "parameter error.")

    # 发布会id不存在
    def test_get_event_error(self):
        r = requests.get(self.url, params={"eid": "1000"})
        result = r.json()
        self.assertEqual(result["status"], 10022)
        self.assertEqual(result["msg"], "query result is empty.")

    # 发布会id为1,查询成功
    def test_get_event_success(self):
        r = requests.get(self.url, params={"eid": "1"})
        result = r.json()
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["msg"], "success.")
        self.assertEqual(result["data"]["name"], "小米5发布会")
        self.assertEqual(result["data"]["address"], "北京国家会议中心")
        # self.assertEqual(result["data"]["start_time"], "2020-12-06T06:00:00Z")


if "__name__" == "__main__":
    unittest.main()