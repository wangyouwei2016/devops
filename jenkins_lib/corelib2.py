# -*- coding:utf-8 -*-
from __future__ import print_function
import jenkins
import para_config
import task_template
import time
import datetime
import statuscode
from home_application.models import jenkins_task_record, deploy_history
from common.log import logger
import os
from jenkins_lib.task_template import template_base_new

#logging.config.fileConfig('mylogging.conf')
#logger = logging.getLogger("jenkins")

server = jenkins.Jenkins(para_config.url, para_config.username, para_config.password, para_config.timeout)


# 创建任务，创建成功返回20010，失败返回20011，任务已经存在返回20011,连接jenkins失败返回10001
#参数job_name表示任务的名称,参数template_type为创建任务选用的模板，默认使用task_template.template_base
def create_job(job_name, job_task_id, template_type):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_FOUND:
        logger.debug(job_name + u'存在，未创建任务。')
        return statuscode.JOB_CREATE_FAILURE
    else:
        logger.info(job_name + u'开始创建。')
        try:
            server.create_job(job_name, template_type)
            time.sleep(10)
            if is_job_exists(job_name):
                logger.debug(job_name + u'创建成功。')
                #jenkins_task_record.objects.get_or_create(task_name=job_name, task_id=job_task_id,
                #                                          task_status=statuscode.JOB_BUILD_NOTBUILT, task_buildnum=0)
                return statuscode.JOB_CREATE_SUCCESS
            else:
                logger.error(job_name + u'创建失败。')
                return statuscode.JOB_CREATE_FAILURE
        except jenkins.JenkinsException as e:
            logger.error(u'创建任务' + job_name + u' 出现异常。' + u' 异常信息：' + e.message)
            return statuscode.JOB_CREATE_FAILURE

# 构建任务，任务开始构建返回:正在构建中，出现异常返回:构建任务异常，任务不存在返回20009,连接jenkins失败返回10001
#参数job_name表示任务的名称
def build_job(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.debug(u'构建未执行，任务没有找到！')
        return statuscode.JOB_NOT_FOUND
    try:
        logger.debug(u'开始构建' + job_name)
        server.build_job(job_name)
        return statuscode.JOB_BUILD_BUILDING
    except jenkins.JenkinsException as e:
        logger.error(u'构建任务' + job_name + u' 出现异常。' + u' 异常信息：' + e.message)
        return statuscode.JOB_BUILD_EXCEPTION

# 构建任务，任务开始构建返回:正在构建中，出现异常返回:构建任务异常，任务不存在返回20009,连接jenkins失败返回10001
# 参数job_name表示任务的名称
def build_job_celery(job_name,job_task_id, svn_url):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.debug(u'构建未执行，任务没有找到！需要先创建任务。')
        template_type = template_base_new(job_name, svn_url)
        if create_job(job_name, job_task_id, template_type) == statuscode.JOB_CREATE_SUCCESS:
            logger.debug(u'任务创建完成，开始构建！')
            pass
        # return statuscode.JOB_NOT_FOUND
    try:
        update_job_base(job_name, svn_url)
        logger.debug(u'在构建' + job_name + u'之前首先更新一下模板...')
        server.build_job(job_name)
        logger.debug(u'开始构建' + job_name)
        time.sleep(15)
        starttime = datetime.datetime.now()
        while is_job_building(job_name):
            time.sleep(para_config.check_build_task_status_time)
            endtime = datetime.datetime.now()
            if (endtime - starttime).seconds > para_config.build_task_timeout:
                logger.warning(u'任务在指定时间内没有完成构建！')
                return statuscode.JOB_BUILD_BUILDING
        build_num = get_last_completed_buildnumber(job_name)
        print(build_num)
        status = statuscode.JOB_BUILD_NOTBUILT
        if is_job_lastbuilt_success(job_name):
            status = statuscode.JOB_BUILD_SUCCESS
            deploy_history.objects.filter(id=job_task_id).update(status="XK待测试")
        if is_job_lastbuilt_failure(job_name):
            status = statuscode.JOB_BUILD_FAILURE
            deploy_history.objects.filter(id=job_task_id).update(status="发布失败")
        if is_job_building(job_name):
            status = statuscode.JOB_BUILD_BUILDING
        try:
            date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            jenkins_task_record.objects.get_or_create(task_name=job_name, task_id=job_task_id,
                                                      task_status=status,
                                                      task_buildnum=build_num, date_added=date_added)
            logger.debug(u"完成异步任务，插入数据库成功!")
        except Exception as e:
            logger.error(u'构建任务' + job_name + u' 数据库插入数据出现异常。' + u' 异常信息：' + e.message)
            return statuscode.JOB_BUILD_EXCEPTION
    except jenkins.JenkinsException as e:
        logger.error(u'构建任务' + job_name + u' 出现异常。' + u' 异常信息：' + e.message)
        return statuscode.JOB_BUILD_EXCEPTION

# 删任务，成功返回20004，失败返回20005，任务不存在返回20009,连接jenkins失败返回10001
#参数job_name表示任务的名称
def delete_job(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.warning(u'删除任务未执行，任务没有找到！')
        return statuscode.JOB_NOT_FOUND

    logger.debug(u'开始删除任务' + job_name)
    try:
        server.delete_job(job_name)
        jenkins_task_record.objects.filter(task_name=job_name).delete()
        logger.debug(u'删除任务：' + job_name + u' 成功。')
        return statuscode.JOB_DEL_SUCCESS
    except jenkins.JenkinsException as e:
        logger.error(u'删除任务' + job_name + u' 出现异常。' + u' 异常信息：' + e.message)
        return statuscode.JOB_DEL_FAILURE

# 获取任务的最后一次构建号，如果任务从未被构建过，返回0
#参数job_name表示任务的名称
def get_last_completed_buildnumber(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.debug(u'获取任务的最后一次构建号码未执行，任务没有找到！')
        return statuscode.JOB_NOT_FOUND
    next_build_num = server.get_job_info(job_name)['nextBuildNumber']
    logger.debug(u'next_build_num is:' + str(next_build_num))
    if next_build_num == 1:
        logger.debug(u'任务还未被执行过。')
        return 0
    else:
        try:
            last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
            return last_build_number
        except Exception as e:
            return 0


# 获取最后一次完成任务的状态信息
# 如果任务被构建成功，返回20000
# 如果任务被构建失败，返回20001
# 如果任务从未被构建过，返回20002
# 如果任务正在构建中，返回20003
#参数job_name表示任务的名称
def get_job_last_buildstatus(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.debug(u'获取任务的状态信息未执行，任务没有找到！')
        return statuscode.JOB_NOT_FOUND
    job_num = get_last_completed_buildnumber(job_name)
    if job_num == 0:
        return statuscode.JOB_BUILD_NOTBUILT

    status = server.get_build_info(job_name, job_num)['result']
    if status == 'SUCCESS':
        logger.debug(u'最后一次完成任务的状态是 — 构建成功。')
        return statuscode.JOB_BUILD_SUCCESS
    else:
        logger.debug(u'最后一次完成任务的状态是 — 构建失败。')
        return statuscode.JOB_BUILD_FAILURE


# 验证任务是否是存在的，存在返回20008，不存在返回20009,连接jenkins失败返回10001
#参数job_name表示任务的名称
def is_job_exists(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if server.job_exists(job_name):
        logger.debug(u"任务：" + job_name + u" 存在。")
        return statuscode.JOB_FOUND
    else:
        logger.debug(u"任务：" + job_name + u" 不存在。")
        return statuscode.JOB_NOT_FOUND


# 验证连接是否成功，成功返回10000，失败返回10001
def is_jenkins_working():
    try:
        server.get_whoami()
        logger.debug(u'登陆jenkins:' + para_config.url + u'成功。')
        return statuscode.CONNECT_JENKINS_SUCCESS
    except jenkins.JenkinsException as e:
        logger.error(u'登陆jenkins:' + para_config.url + u' 出现异常，请确认网络、用户名和密码信息！' +
                      u' 异常信息：' + e.message)
        return statuscode.CONNECT_JENKINS_FAIL

# 验证任务是否正在构建，是返回True，否返回false
#参数job_name表示任务的名称
def is_job_building(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        logger.error(u'连接Jekins失败 ！')
        return False

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.error(u'查看任务是否正在构建未执行！没有找到指定任务。')
        return False

    last_num = get_last_completed_buildnumber(job_name)

    try:
        server.get_build_info(job_name, last_num + 1)['building']
        logger.info(job_name + u' 正在构建。')
        return True
    except jenkins.JenkinsException as e:
        logger.info(job_name + u' 未在构建。')
        return False

# 验证任务最后一次构建是否成功，是返回True，否返回false
# 任务从未构建返回20002
# 参数job_name表示任务的名称
def is_job_lastbuilt_success(job_name):

    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        logger.error(u'连接Jekins失败 ！')
        return False

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.error(u'查看任务是否正在构建未执行！没有找到指定任务。')
        return False

    job_num = get_last_completed_buildnumber(job_name)

    if job_num == 0:
        logger.warning(u'任务尚未构建。')
        return False

    status = server.get_build_info(job_name, job_num)['result']
    if status == 'SUCCESS':
        logger.debug(u'最后一次完成任务的状态是 — 构建成功。')
        return True
    else:
        logger.debug(u'最后一次完成任务的状态是 — 构建失败。')
        return False

# 验证任务最后一次构建是否失败，是返回True，否返回false
# 参数job_name表示任务的名称
def is_job_lastbuilt_failure(job_name):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        logger.error(u'连接Jekins失败 ！')
        return False

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.error(u'查看任务是否正在构建未执行！没有找到指定任务。')
        return False

    job_num = get_last_completed_buildnumber(job_name)

    if job_num == 0:
        logger.warning(u'任务尚未构建。')
        return False

    status = server.get_build_info(job_name, job_num)['result']
    if status == 'FAILURE':
        logger.debug(u'最后一次完成任务的状态是 — 构建失败。')
        return True
    else:
        logger.debug(u'最后一次完成任务的状态是 — 构建成功。')
        return False

# 获取任务的构建状态，任务构建成功返回:构建成功，任务构建失败返回:构建失败，任务尚未构建返回：尚未构建，任务构建中返回：正在构建中
# 任务不存在返回20009,任务版本号错误返回20003，连接jenkins失败返回10001 ，
#参数job_name表示任务的名称；参数build_num表示任务的构建版本号
def get_job_build_status(job_name, build_num):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        return statuscode.CONNECT_JENKINS_FAIL

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.warning(u'获取任务的状态信息未执行，任务没有找到！')
        return statuscode.JOB_NOT_FOUND
    job_num = get_last_completed_buildnumber(job_name)
    if job_num == 0:
        return statuscode.JOB_BUILD_NOTBUILT
    try:
        status = server.get_build_info(job_name, build_num)['result']
    except jenkins.JenkinsException as e:
        logger.error(u'获取任务的构建信息出现异常:任务: '+job_name+ u' 构建版本:'+ str(build_num)+ u' 异常信息:' + e.message)
        return statuscode.JOB_BUILD_NUM_EXCEPTION

    if status == 'FAILURE':
        return statuscode.JOB_BUILD_FAILURE
    elif status == 'SUCCESS':
        return statuscode.JOB_BUILD_SUCCESS
    else:
         return statuscode.JOB_BUILD_BUILDING


# 更新任务模板，成功返回:True，失败返回:False
# 参数job_name表示任务的名称；参数template_type表示使用的任务模板
def update_job_base(job_name, svn_url):
    if is_jenkins_working() == statuscode.CONNECT_JENKINS_FAIL:
        logger.error(u'连接Jekins失败 ！')
        return False

    if is_job_exists(job_name) == statuscode.JOB_NOT_FOUND:
        logger.warning(u'获取任务的状态信息未执行，任务没有找到！')
        return False

    try:
        template_type = template_base_new(job_name, svn_url)
        server.reconfig_job(job_name, template_type)
        return True
    except jenkins.JenkinsException as e:
        logger.error(u'重新配置任务' + job_name + u' 出现异常。' + u' 异常信息：' + e.message)
        return False

# 获取job名为job_name的job指定build_id的构建output信息
def get_jenkins_jobs_output(job_name, build_number):
    last_build_output = server.get_build_console_output(job_name, build_number)
    return last_build_output

#获取job名为job_name的job的最后次构建号
def get_jenkins_job_lastbuild_number(job_name):
    last_build_number = server.get_job_info(job_name)['lastBuild']['number']
    return last_build_number