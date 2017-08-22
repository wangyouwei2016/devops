# -*- coding: utf-8 -*-

from django.db import models

class jenkins_task_record(models.Model):
    task_name=models.CharField(u"任务名称", max_length=100)
    task_id=models.IntegerField(u"任务id")
    task_status=models.CharField(u"任务状态", max_length=20)
    task_buildnum = models.IntegerField(u"任务构建版本号")

    def __unicode__(self):
        return self.task_name