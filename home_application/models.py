# -*- coding: utf-8 -*-

from django.db import models

class applications(models.Model):
    business_id = models.CharField(u"业务线ID", max_length=20)
    business_name = models.CharField(u"业务线名称", max_length=40)
    name = models.CharField(u"应用名称", max_length=100)
    version_id = models.CharField(u"版本id", max_length=20)
    version_name = models.CharField(u"版本名称", max_length=40)
    master = models.CharField(u"产品master", max_length=64)
    owner = models.CharField(u"应用owner", max_length=64)
    svn_path = models.CharField(u"svn地址", max_length=240)
    depend_app = models.CharField(u"依赖的应用", max_length=64)
    depend_by = models.CharField(u"谁依赖", max_length=64)
    target_server_ip = models.CharField(u"目标部署服务器ip", max_length=80)
    deploy_path = models.CharField(u"应用部署目录", max_length=100)
    war_name = models.CharField(u"应用war包名称", max_length=64)
    war_path = models.CharField(u"应用war包路径", max_length=64)
    sequence = models.CharField(u"内部版本序列号", max_length=20)
    config_path = models.CharField(u"配置文件路径", max_length=80)
    type = models.CharField(u"应用类型", max_length=10) # web  or 手机app
    cluster_num = models.CharField(u"集群数量", max_length=2)
    status = models.CharField(u"应用状态", max_length=10) # 1  新建 2  更新  3下线
    operator = models.CharField(u"维护者", max_length=20)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'applications'

    def __unicode__(self):
        return self.name
'''
业务线与应用 一对多
'''
class business_applications(models.Model):
    business = models.CharField(u"业务线", max_length=20)
    master = models.CharField(u"产品master", max_length=64)
    owner = models.CharField(u"应用owner", max_length=64)
    application_id = models.CharField(u"应用id", max_length=20)
    application = models.CharField(u"应用", max_length=20)
    discription = models.TextField(u"描述", max_length=128)

    class Meta:
        db_table = u'business_applications'

    def __unicode__(self):
        return self.business

class applications_config(models.Model):
    business = models.CharField(u"业务线", max_length=20)
    application_id = models.CharField(u"应用id", max_length=20)
    master = models.CharField(u"产品master", max_length=64)
    owner = models.CharField(u"应用owner", max_length=64)
    config_path = models.CharField(u"配置文件路径", max_length=80)
    type = models.CharField(u"应用类型", max_length=10) # web  or 手机app
    operator = models.CharField(u"维护者", max_length=20)

    class Meta:
        db_table = u'applications_config'

    def __unicode__(self):
        return self.business

class applications_config_item(models.Model):
    config_id = models.CharField(u"配置id", max_length=20)
    business = models.CharField(u"业务线", max_length=20)
    master = models.CharField(u"产品master", max_length=64)
    owner = models.CharField(u"应用owner", max_length=64)
    config_path = models.CharField(u"配置文件路径", max_length=80)
    item_key = models.CharField(u"配置项key", max_length=40)
    item_value = models.CharField(u"配置项value", max_length=100)

    class Meta:
        db_table = u'applications_config_item'

    def __unicode__(self):
        return self.config_id

class business_info(models.Model):
    name = models.CharField(u"业务线名称", max_length=20)
    master = models.CharField(u"业务线master", max_length=64)
    discription = models.TextField(u"描述", max_length=128)

    class Meta:
        db_table = u'business_info'

    def __unicode__(self):
        return self.name

class deploy_history(models.Model):
    business_id = models.CharField(u"业务线ID", max_length=20)
    business_name = models.CharField(u"业务线名称", max_length=40)
    applications_id = models.CharField(u"应用ID", max_length=20)
    applications_name = models.CharField(u"应用名称", max_length=20)
    release_version = models.CharField(u"申请版本号", max_length=20)
    latest_version = models.CharField(u"线上版本号", max_length=20)
    release_reason = models.CharField(u"发布理由", max_length=40)
    pre_release_time = models.DateTimeField(auto_now=False)
    applicant = models.CharField(u"申请人", max_length=64)
    svn_path = models.CharField(u"svn地址", max_length=240)
    war_name = models.CharField(u"应用war包名称", max_length=64)
    war_path = models.CharField(u"应用war包路径", max_length=64)
    sequence = models.CharField(u"内部版本序列号", max_length=20)
    type = models.CharField(u"应用类型", max_length=10) # 1.web  or 2.手机app or 3.接口
    status = models.CharField(u"应用状态", max_length=10) # 1 申请 2 XK待测试  3 线上待发布 4 线上待测试 5 完成 6 退回 7 回滚
    tester = models.CharField(u"测试人", max_length=20)
    reviewer = models.CharField(u"审核人", max_length=20)
    operator = models.CharField(u"维护者", max_length=20)
    email_address = models.CharField(u"关系人邮件", max_length=240)
    remote_ip = models.CharField(u"登录IP地址", max_length=64)
    date_added = models.DateTimeField(auto_now=True)
    date_tested = models.DateTimeField(auto_now=False)
    date_reviewed = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = u'deploy_history'

    def __unicode__(self):
        return self.applications_id

class status_info(models.Model):
    name = models.CharField(u"状态名称", max_length=20)
    instraction = models.CharField(u"状态说明", max_length=64)
    discription = models.TextField(u"备注", max_length=128)

    class Meta:
        db_table = u'status_info'

    def __unicode__(self):
        return self.name