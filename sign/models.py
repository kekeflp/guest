from django.db import models


# Create your models here.
# id自动生成并且自增
# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    start_time = models.DateTimeField('event time')
    # 创建时间(自动获取当前时间)
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 嘉宾表
class Guest(models.Model):
    # 外键,关联发布会id
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "phone")

    def __str__(self):
        return self.real_name
