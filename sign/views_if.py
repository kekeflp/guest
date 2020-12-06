import re
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from sign.models import Event, Guest
from django.db.utils import IntegrityError
import time


# 添加发布会的接口
def add_event(request):
    # 发布会ID
    eid = request.POST.get("eid", "")
    name = request.POST.get("name", "")
    limit = request.POST.get("limit", "")
    status = request.POST.get("status", "")
    address = request.POST.get("address", "")
    start_time = request.POST.get("start_time", "")

    if eid == "" or name == "" or limit == "" or status == "" or address == "" or start_time == "":
        return JsonResponse({"status": 10021, "msg": "parameter error."})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({
            "status": 10022,
            "msg": "event id already exists."
        })

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({
            "status": 10023,
            "msg": "event name already exists."
        })

    # 非必须数据, 可以设置默认值
    if status == "":
        status = 1

    try:
        Event.objects.create(id=eid,
                             name=name,
                             limit=limit,
                             status=int(status),
                             address=address,
                             start_time=start_time)
    except ValidationError as e:
        return JsonResponse({
            "status":
            10024,
            "msg":
            "start_time format error. It must be in YYYY-MM-DD HH:MM:SS format."
        })

    return JsonResponse({"status": 200, "msg": "add event success."})


# 添加嘉宾的接口
def add_guest(request):
    # 发布会ID
    eid = request.POST.get("eid", "")
    real_name = request.POST.get("real_name", "")
    phone = request.POST.get("phone", "")
    email = request.POST.get("email", "")

    if eid == "" or real_name == "" or phone == "" or email == "":
        return JsonResponse({"status": 10021, "msg": "parameter error."})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({"status": 10022, "msg": "event id null."})

    result = Event.objects.get(id=eid).status
    if result:
        return JsonResponse({
            "status": 10023,
            "msg": "event status is not available."
        })

    # 人数比较
    # 发布会限制人数
    event_limit = Event.objects.get(id=eid).limit
    # 发布会已添加的嘉宾数
    guest_limit = Guest.objects.filter(event_id=eid)
    if len(guest_limit) >= event_limit:
        return JsonResponse({"status": 10024, "msg": "event number is full."})

    # 时间比较
    # 发布会开始时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))
    # 当前时间
    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time > e_time:
        return JsonResponse({"status": 10025, "msg": "event has started."})

    try:
        Guest.objects.create(event_id=int(eid),
                             real_name=real_name,
                             phone=int(phone),
                             email=email,
                             sign=0)
    except IntegrityError:
        return JsonResponse({
            "status": 10026,
            "msg": "the event guest phone number repeat."
        })

    return JsonResponse({"status": 200, "msg": "add guest success."})


# 查询发布会的接口
def get_event_list(request):
    eid = request.GET.get("eid", "")
    name = request.GET.get("name", "")

    if eid == "" and name == "":
        return JsonResponse({"status": 10021, "msg": "parameter error."})

    if eid != "":
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({
                "status": 10022,
                "msg": "query result is empty."
            })
        else:
            event["name"] = result.name
            event["limit"] = result.limit
            event["status"] = result.status
            event["address"] = result.address
            event["start_time"] = result.start_time
            return JsonResponse({
                "status": 200,
                "msg": "success.",
                "data": event
            })

    if name != "":
        # 声明一个数组
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                # 声明一个字典
                event = {}
                event["name"] = r.name
                event["limit"] = r.limit
                event["status"] = r.status
                event["address"] = r.address
                event["start_time"] = r.start_time
                datas.append(event)
            return JsonResponse({
                "status": 200,
                "msg": "success.",
                "data": datas
            })
        else:
            return JsonResponse({
                "status": 10022,
                "msg": "query result is empty."
            })


# 查询嘉宾的接口
def get_guest_list(request):
    # 关联发布会的id
    eid = request.GET.get("eid", "")
    phone = request.GET.get("phone", "")

    if eid == "":
        return JsonResponse({
            "status": 10021,
            "msg": "event_id cannot be empty."
        })

    if eid != "" and phone != "":
        guest = {}
        try:
            result = Guest.objects.get(phone=phone, event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({
                "status": 10022,
                "msg": "query result is empty."
            })
        else:
            guest["real_name"] = result.real_name
            guest["phone"] = result.phone
            guest["email"] = result.email
            guest["sign"] = result.sign
            return JsonResponse({
                "status": 200,
                "msg": "success.",
                "data": guest
            })

    if eid != "" and phone == "":
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                # 声明一个字典
                guest = {}
                guest["real_name"] = r.real_name
                guest["phone"] = r.phone
                guest["email"] = r.email
                guest["sign"] = r.sign
                datas.append(guest)
            return JsonResponse({
                "status": 200,
                "msg": "success.",
                "data": datas
            })
        else:
            return JsonResponse({
                "status": 10022,
                "msg": "query result is empty."
            })


# 嘉宾签到的接口
def user_sign(request):
    eid = request.POST.get("eid", "")
    phone = request.POST.get("phone", "")

    if eid == "" and phone == "":
        return JsonResponse({"status": 10021, "msg": "parameter error."})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({"status": 10022, "msg": "event id null."})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({
            "status": 10023,
            "msg": "event status is not avilable."
        })

    # 时间比较
    # 发布会开始时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))
    # 当前时间
    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time > e_time:
        return JsonResponse({"status": 10024, "msg": "event has started."})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({"status": 10025, "msg": "user phone null."})

    result = Guest.objects.filter(event_id=eid, phone=phone)
    if not result:
        return JsonResponse({
            "status":
            10026,
            "msg":
            "user did not participate in the conference."
        })

    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if not result:
        return JsonResponse({"status": 10027, "msg": "user has sign in."})
    else:
        Guest.objects.filter(event_id=eid, phone=phone).update(sign="1")
        return JsonResponse({"status": 200, "msg": "sign success."})
