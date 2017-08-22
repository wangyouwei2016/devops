# -*- coding:utf-8 -*-
import corelib2
import os

import time
import datetime
from home_application import celery_tasks
from home_application.models import deploy_history
from home_application.json_template import json_template_base

from celery import task
#print corelib2.create_job('db_test5',123456)
#print corelib2.build_job('db_test5')
#print corelib2.build_job_celery('demo_script2')
#celery_tasks.build_task.delay('db_test5')
#print corelib2.build_job_celery('crimport',456789088)
#print celery_tasks.build_task.delay('demo_script2',4567100)   #异步构建任务
#print 'hello'
#print corelib2.create_job('crimport',123456, 'http://10.32.151.33:6080/svn/xikang/11熙康开放平台/Trunk/02.代码库/phr/CRImport')
#print celery_tasks.build_task.delay('crimport-devops', 285, 'http://10.32.151.33:6080/svn/xikang/11熙康开放平台/Trunk/02.代码库/phr/CRImport')   #异步构建任务
# print corelib2.get_jenkins_jobs_output("crimport-devops", 14)
# celery_tasks.xk_deploy.delay('300', 'crimport-devops/XK/20170804/crimport.war', 'crimport-devops')
#print corelib2.delete_job("db_test2")


'''
import datetime
starttime = datetime.datetime.now()
#long running
time.sleep(5)
endtime = datetime.datetime.now()

print (endtime-starttime).seconds
#print (endtime–starttime).seconds
'''