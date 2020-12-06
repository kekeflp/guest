from logging import setLogRecordFactory
import re
from sign.views import guest_manage
from django.contrib.auth.models import User
from django.test import TestCase
from sign.models import Guest, Event


# Create your tests here.
# 构造虚拟表数据的测试用例
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=10,
                             name="oneplus 3 发布会",
                             limit=200,
                             status=True,
                             address="深圳",
                             start_time="2020-08-31 14:00:00")
        Guest.objects.create(id=10,
                             event_id=10,
                             real_name="刘德华",
                             phone=10010001111,
                             sign=False,
                             email="liudehua@mail.com")

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 发布会")
        self.assertEqual(result.address, "深圳")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone=10010001111)
        self.assertEqual(result.real_name, "刘德华")
        self.assertFalse(result.sign)


# 测试 index 登录首页
class IndexPageTest(TestCase):
    def test_index_page_render_index_template(self):
        # 测试 index.html 视图
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "index.html")


# 测试登录动作
class LoginActionTest(TestCase):
    def setUp(self):
        # 创建用户
        User.objects.create_user("admin", "admin@mail.com", "admin123456")

    def test_add_admin(self):
        # 测试添加的用户
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        # 测试用户名密码为空的场景
        # 创建一个字典
        # uid/pwd 字段需要与页面上一致
        test_data = {"uid": "", "pwd": ""}
        response = self.client.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 200)
        # 原 index.html 中定义的 error为字符串,
        # 而 response.content 返回的是字节,所以需要转换
        str = "用户名或密码错误!"
        self.assertIn(bytes(str, encoding="utf8"), response.content)

    def test_login_action_username_password_error(self):
        # 测试用户名密码错误的场景
        test_data = {"uid": "123123", "pwd": "1342342"}
        response = self.client.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 200)
        str = "用户名或密码错误!"
        self.assertIn(bytes(str, encoding="utf8"), response.content)

    def test_login_action_success(self):
        # 测试用户名密码为正常的场景
        test_data = {"uid": "admin", "pwd": "admin123456"}
        response = self.client.post("/login_action/", data=test_data)
        self.assertEqual(response.status_code, 302)


# 测试发布会管理
class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")
        self.login_user = {"uid": "admin", "pwd": "admin123456"}
        Event.objects.create(id=5,
                             name="小米8Pro发布会",
                             limit=200,
                             status=True,
                             address="深圳",
                             start_time="2020-08-31 14:00:00")

    def test_event_manage_success(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/event_manage/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("小米8Pro发布会", encoding="utf8"), response.content)
        self.assertIn(bytes("深圳", encoding="utf8"), response.content)

    def test_event_manage_search_success(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/search_name/", {"name": "小米8Pro发布会"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("小米8Pro发布会", encoding="utf8"), response.content)
        self.assertIn(bytes("深圳", encoding="utf8"), response.content)


# 测试嘉宾管理
class GuestManageTest(TestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")
        self.login_user = {"uid": "admin", "pwd": "admin123456"}
        Event.objects.create(id=5,
                             name="小米8Pro发布会",
                             limit=200,
                             status=True,
                             address="深圳",
                             start_time="2020-12-03 06:00:00")
        Guest.objects.create(id=10,
                             event_id=5,
                             real_name="刘德华",
                             phone=10010001111,
                             sign=False,
                             email="liudehua@mail.com")

    def test_guest_manage_success(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/guest_manage/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("刘德华", encoding="utf8"), response.content)
        self.assertIn(bytes("10010001111", encoding="utf8"), response.content)

    def test_guest_manage_search_name_success(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/search_guest_name/", {"name": "刘德华"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("刘德华", encoding="utf8"), response.content)
        self.assertIn(bytes("小米8Pro发布会", encoding="utf8"), response.content)

# 发布会签到
class SignIndexActionTest(TestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")
        self.login_user = {"uid": "admin", "pwd": "admin123456"}
        Event.objects.create(id=1,
                             name="小米8Pro发布会",
                             limit=200,
                             status=1,
                             address="深圳",
                             start_time="2020-12-01 06:00:00")
        Event.objects.create(id=2,
                             name="Apple8+发布会",
                             limit=500,
                             status=1,
                             address="北京",
                             start_time="2020-12-02 06:00:00")
        Guest.objects.create(id=1,
                             event_id=1,
                             real_name="刘德华",
                             phone=10010001111,
                             sign=0,
                             email="liudehua@mail.com")
        Guest.objects.create(id=2,
                             event_id=2,
                             real_name="张学友",
                             phone=10010002222,
                             sign=1,
                             email="zhangxueyou@mail.com")

    def test_sign_index_action_phone_null(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/sign_index_action/1/", {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("电话号码错误!", encoding="utf8"), response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/sign_index_action/2/", {"phone": "10010001111"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("发布会id或电话号码错误!", encoding="utf8"), response.content)

    def test_sign_index_action_user_sign_has(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/sign_index_action/2/", {"phone": "10010002222"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("用户已签到!", encoding="utf8"), response.content)

    def test_sign_index_action_sign_success(self):
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/sign_index_action/1/", {"phone": "10010001111"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(bytes("用户签到成功!", encoding="utf8"), response.content)