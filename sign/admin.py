from django.contrib import admin
from sign.models import Event, Guest


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    # 列头显示字段
    list_display = ['id', 'name', 'limit', 'status', 'address', 'start_time']
    # 搜索栏
    search_fields = ['name']
    # 过滤器
    list_filter = ['status']


class GuestAdmin(admin.ModelAdmin):
    list_display = ['real_name', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['real_name', 'phone']
    list_filter = ['sign']


# 用EventAdmin选项注册Event模块
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
