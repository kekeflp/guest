import re
import sign
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

# Create your views here.
# 定义index视图, 通过请求返回一个对象
def index(request):
    # 返回 通过响应,返回文本对象
    # return HttpResponse("Hello world!")
    # 返回 通过请求,返回文件对象
    return render(request, "index.html")


# 登录动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("uid", "")
        password = request.POST.get("pwd", "")
        # 与数据库中username和password字段比较, 如果存在一致则返回对象, 不一致则返回None
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # 登录
            auth.login(request, user)
            response = HttpResponseRedirect("/event_manage/")
            # response.set_cookie("user", username, 300)
            request.session["user"] = username
            return response
        else:
            return render(request, "index.html", {"error": "用户名或密码错误!"})


# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get("user", "")
    username = request.session.get("user", "")
    return render(request, "event_manage.html", {
        "user": username,
        "events": event_list
    })


# 发布会搜索
@login_required
def search_name(request):
    username = request.session.get("user", "")
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {
        "user": username,
        "events": event_list
    })


# 嘉宾管理
# @login_required
# def guest_manage(request):
#     guest_list = Guest.objects.all()
#     # username = request.COOKIES.get("user", "")
#     username = request.session.get("user", "")
#     return render(request, "guest_manage.html", {
#         "user": username,
#         "guests": guest_list
#     })


@login_required
def guest_manage(request):
    username = request.session.get("user", "")
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 10)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {
        "user": username,
        "guests": contacts
    })


# 嘉宾搜索
@login_required
def search_guest_name(request):
    username = request.session.get("user", "")
    search_name = request.GET.get("name", "")
    guest_list = Guest.objects.filter(real_name__contains=search_name)
    return render(request, "guest_manage.html", {
        "user": username,
        "guests": guest_list
    })


# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, "sign_index.html", {"event": event})


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get("phone", "")
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, "sign_index.html", {
            "event": event,
            "hint": "电话号码错误!"
        })
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, "sign_index.html", {
            "event": event,
            "hint": "发布会id或电话号码错误!"
        })
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, "sign_index.html", {
            "event": event,
            "hint": "用户已签到!"
        })
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign="1")
        return render(request, "sign_index.html", {
            "event": event,
            "hint": "用户签到成功!",
            "guest": result
        })


# 退出
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect("/index/")
    return response