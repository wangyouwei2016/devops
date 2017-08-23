# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_mako
import MySQLdb
from account.models import BkUser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from home_application.models import applications, business_info, deploy_history, deploy_status_history, jenkins_task_record, business_applications, applications_config, applications_config_item
from home_application.api import pages, my_render, ServerError, get_object, db_add_applications
from django.shortcuts import render
from common.log import logger
import datetime
import time
import os
import deploy_statuscode
from json_template import json_template_base_business, json_template_base_month
from django.template.context_processors import csrf
# from ansible_playbook_api import ansible_play
from home_application.mysql2json_api import TableToJson
from jenkins_lib.corelib2 import get_jenkins_jobs_output, get_jenkins_job_lastbuild_number
from home_application.celery_tasks import build_task, xk_deploy, sc_deploy

def compute(request):

    result = get_table('10.32.144.182', 'root', 'tongze@2011', 3306)
    # print '1', result
    # for s in result:
    #     print s
    return render_to_response('home_application/monitor.html', locals(), context_instance=RequestContext(request))

def get_table(ip, user, passwd, port):
    try:
        conn = MySQLdb.connect(host=ip, user=user, passwd=passwd, db="itoss",
                               connect_timeout=10, port=int(port), charset='utf8')
        cur = conn.cursor()

        #sql = "SELECT t.Person_PHR_Code, t.Person_Name, t.Birthday, t.Gender_Name, t.Person_Nickname,  t.Name_Spell, t.Change_Time FROM acornhc_healthdata.phr_person_basic_info t limit 10"

        sql = "SELECT m.CreatedDateTime,m.StatusCreateTime,m.EquipmentId,m.RecId,m.MonitorStatus,m.Title,m.MonitorValue,m.MonitorType,m.LastModDateTime,m.IsDisabled,a.ETitle,a.ServerAddress,a.GroupName,a.gId FROM Monitor m LEFT JOIN (SELECT e.RecId AS ERecId,e.title AS ETitle,e.ServerAddress,g.GroupName,g.RecId gId FROM Equipment e LEFT JOIN EccGroup g ON e.GroupId = g.RecId) a ON m.equipmentid = a.ERecId WHERE (m.MonitorStatus = 'error' OR m.MonitorStatus = 'warning')AND m.IsDisabled = 0 ORDER BY m.MonitorStatus"

        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return result


def get_urllist(ip, user, passwd, port):
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()

        #sql = "SELECT t.Person_PHR_Code, t.Person_Name, t.Birthday, t.Gender_Name, t.Person_Nickname,  t.Name_Spell, t.Change_Time FROM acornhc_healthdata.phr_person_basic_info t limit 10"

        sql = "SELECT * FROM monitor_url_status"
        cur.execute(sql)
        urldb = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e
    except Exception, e1:
        print e1
    return urldb

def get_error():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT COUNT(*) FROM monitor_url_status WHERE HttpCode != 200 AND HttpCode !=302 "
        cur.execute(sql)
        errorcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return errorcount


def get_urlslow():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT COUNT(*) FROM monitor_url_status WHERE TotalTime > 2000 "
        cur.execute(sql)
        urlslow = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return urlslow

def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')

def index(request):
    """
    新版首页
    """
    result = get_table('10.32.144.182', 'root', 'tongze@2011', 3306)
    # print '1',result
    # for s in result:
    #     print s
    procount = get_procount()[0]
    xkcount = get_xkcount()[0]
    jccount = get_jccount()[0]
    zbcount = get_zbcount()[0]
    proappcount = get_proappcount()[0]
    xkappcount = get_xkappcount()[0]
    allcount1 = xkcount + jccount + procount + zbcount + 5
    zcptccount = get_zcptccount()[0]
    zcptczj = get_zcptczj()[0][0]
    zsyyy = get_zcptczj()[1][0]
    zsyyyzj = get_zcptczj()[2][0]
    clhis = get_zcptczj()[3][0]
    clhiszj = get_zcptczj()[4][0]
    csyyy = get_zcptczj()[5][0]
    csyyyzj = get_zcptczj()[6][0]
    jgzx = get_zcptczj()[7][0]
    jgzxzj = get_zcptczj()[8][0]
    ylhl = get_zcptczj()[9][0]
    ylhlzj = get_zcptczj()[10][0]
    ycxd = get_zcptczj()[11][0]
    ycxdzj = get_zcptczj()[12][0]
    jkcs = get_zcptczj()[13][0]
    jkcszj = get_zcptczj()[14][0]
    ikeep = get_zcptczj()[15][0]
    ikeepzj = get_zcptczj()[16][0]
    isleep = get_zcptczj()[17][0]
    isleepzj = get_zcptczj()[18][0]
    xkw = get_zcptczj()[19][0]
    xkwzj = get_zcptczj()[20][0]
    qita = get_zcptczj()[21][0]
    qitazj = get_zcptczj()[22][0]
    hygeaipall = get_hygeaipall()
    apphybrid = get_apphybridipall()
    loadstatus = get_loadstatus()
    #print loadstatus

    # print '1', result
    # for s in result:
    #     print s
    # 统计当月发版总数：
    cur = datetime.datetime.now()
    this_month = cur.month
    all_counts = deploy_history.objects.filter(date_added__month=this_month).count()

    # 统计版本分发次数（发版成功次数）：
    success_counts = deploy_history.objects.filter(date_added__month=this_month).filter(
        status=deploy_statuscode.DEPLOY_FIFTH_STATUS).count()

    # 统计退回次数：
    return_counts = deploy_history.objects.filter(date_added__month=this_month).filter(
        Q(status=deploy_statuscode.TEST_SC_RETURN_STATUS) | Q(status=deploy_statuscode.TEST_XK_RETURN_STATUS) | Q(
            status=deploy_statuscode.REVIEW_BACK_STATUS)).count()

    # 版本分发失败率：
    fail_counts = deploy_history.objects.filter(date_added__month=this_month).filter(
        Q(status=deploy_statuscode.DEPLOY_FAILED_STATUS) | Q(status=deploy_statuscode.ROLLBACK_STATUS)).count()
    if fail_counts ==0 or all_counts == 0:
        fail_percent =0
    else:
        fail_percent = '%.2f' % (float(fail_counts) / float(all_counts))

    # 按业务线统计：
    business_counts1 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=1).count()
    business_counts2 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=2).count()
    business_counts3 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=3).count()
    business_counts4 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=4).count()
    business_counts5 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=5).count()
    business_counts6 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=6).count()
    business_counts7 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=7).count()
    business_counts8 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=8).count()
    business_counts9 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=9).count()
    business_counts10 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=10).count()
    business_counts11 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=11).count()
    business_counts12 = deploy_history.objects.filter(date_added__month=this_month).filter(business_id=12).count()
    json_template_base_business(business_counts1, business_counts2, business_counts3, business_counts4,
                                business_counts5,
                                business_counts6, business_counts7, business_counts8, business_counts9,
                                business_counts10,
                                business_counts11, business_counts12)

    # 按月份统计：
    all_month_counts = []
    success_month_counts = []
    for i in range(1, 13):
        month_count = [deploy_history.objects.filter(date_added__month=i).count()]
        print month_count
        all_month_counts = all_month_counts + month_count
        print all_month_counts
    for j in range(1, 13):
        success_month_count = [deploy_history.objects.filter(date_added__month=j).filter(
            status=deploy_statuscode.DEPLOY_FIFTH_STATUS).count()]
        print success_month_count
        success_month_counts = success_month_counts + success_month_count
    json_template_base_month(all_month_counts, success_month_counts)

    return render_to_response('home_application/index.html', locals(), context_instance=RequestContext(request))
def operation(request):
    """
    发布列表
    """
    return render_mako_context(request, '/home_application/operation.html')

def header(request):
    """
    页面头部
    """
    return my_render('home_application/header.html', locals(), request)

def menu(request):
    """
    菜单列表
    """
    return my_render('home_application/menu.html', locals(), request)

def Return_Apps_Data(request):
    business_id = request.GET['business_select']
    print business_id
    app_list = applications.objects.filter(business_id=business_id)
    return HttpResponse(app_list)

def apply(request):
    """
    发布申请
    """
    username = request.user.username
    user_email = BkUser.objects.get(username=username).email
    remote_ip = request.META.get('REMOTE_ADDR')
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    business_list = business_info.objects.all().order_by("name")
    business_select = request.GET.get('business_select1', '')
    applications_list = applications.objects.all().order_by("name")

    if request.method == 'POST':
        business_name = request.POST.get('business_select1', '')
        applications_name = request.POST.get('app_select1', '')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        release_version = request.POST.get('version_id')
        release_reason = request.POST.get('release_reason', '')
        email_address_post = request.POST.get('email_address_post', '')
        email_address = user_email + ',' + email_address_post
        app_type = request.POST.get('app_type', '')
        jenkins_select = request.POST.get('jenkins_select','300')

        try:
            if business_name == "":
                emg = u'业务线不能为空！'
            else:
                business_id = business_info.objects.get(name=business_name).id
                if applications_name == "":
                    emg = u'应用名称不能为空！'
                else:
                    applications_id = applications.objects.get(name=applications_name).id
                    svn_path = applications.objects.get(id=applications_id).svn_path
                    deploy_version = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")).lstrip("20")
                    operator = applications.objects.get(id=applications_id).operator
                    latest_version = applications.objects.get(id=applications_id).version_id
                    if jenkins_select == '200':
                        deploy_history.objects.create(business_id=business_id, business_name=business_name,
                                           applications_id=applications_id, applications_name=applications_name,
                                           release_version=release_version, release_reason=release_reason,
                                           latest_version=latest_version, applicant=username, deploy_version=deploy_version,
                                           operator=operator, remote_ip=remote_ip, svn_path=svn_path, war_path=war_path,
                                           status=deploy_statuscode.DEPLOYING_XK_STATUS, email_address=email_address, jenkins_select=jenkins_select,
                                           type=app_type, war_name=war_name, date_added=date_added)
                        time.sleep(2)
                        task_id = deploy_history.objects.get(deploy_version=deploy_version).id
                        deploy_status_history.objects.create(task_id=312, app_name=applications_name,
                                                             pre_status=deploy_statuscode.DEPLOY_FIRST_STATUS,
                                                             new_status=deploy_statuscode.DEPLOYING_XK_STATUS,
                                                             operator=username)
                        print "################starting building##################"
                        build_task.delay(applications_name, task_id, svn_path)
                        smg = u"应用 %s 已提交到jenkins打版，将自动发布到XK环境。" % applications_name
                        # return HttpResponse(smg)
                    else:
                        if war_path == "":
                            emg = u'不需要在线打包时，程序包位置不能为空！'
                        else:
                            deploy_history.objects.create(business_id=business_id, business_name=business_name,
                                               applications_id=applications_id, applications_name=applications_name,
                                               release_version=release_version, release_reason=release_reason,
                                               latest_version=latest_version, applicant=username, deploy_version=deploy_version,
                                               operator=operator, remote_ip=remote_ip, svn_path=svn_path, war_path=war_path,
                                               status=deploy_statuscode.DEPLOYING_XK_STATUS, email_address=email_address, jenkins_select=jenkins_select,
                                               type=app_type, war_name=war_name, date_added=date_added)
                            time.sleep(2)
                            print "################start deploying##################"
                            task_id = deploy_history.objects.get(deploy_version=deploy_version).id
                            deploy_status_history.objects.create(task_id=task_id, app_name=applications_name,
                                                                 pre_status=deploy_statuscode.DEPLOY_FIRST_STATUS,
                                                                 new_status=deploy_statuscode.DEPLOYING_XK_STATUS,
                                                                 operator=username)
                            if xk_deploy.delay(task_id, war_path, applications_name):
                                smg = u'应用 %s 发布成功！' % applications_name
                            else:
                                deploy_history.objects.filter(id=task_id).update(status="发布失败")
                                emg = u'应用 %s 发布失败，请联系管理员！' % applications_name
                            smg = u'应用 %s 发布申请已提交！将自动发布至XK环境！' % applications_name
        except ServerError:
            pass

    return my_render('home_application/apply.html', locals(), request)

def apply_bak(request):
    """
    发布申请
    """
    username = request.user.username
    user_email = BkUser.objects.get(username=username).email
    remote_ip = request.META.get('REMOTE_ADDR')
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    business_list = business_info.objects.all().order_by("name")
    business_select = request.GET.get('business_select', '')
    applications_list = applications.objects.all().order_by("name")

    if request.method == 'POST':
        business_id = request.POST.get('business_select', '')
        applications_id = request.POST.get('app_select', '')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        release_version = request.POST.get('version_id')
        release_reason = request.POST.get('release_reason', '')
        email_address_post = request.POST.get('email_address_post', '')
        email_address = user_email + ',' + email_address_post
        status = "提交申请"
        app_type = request.POST.get('app_type', '')
        jenkins_select = request.POST.get('jenkins_select', '300')

        try:
            if business_id == "":
                emg = u'业务线不能为空！'
            else:
                business_name = business_info.objects.get(id=business_id).name
                if applications_id == "":
                    emg = u'应用名称不能为空！'
                else:
                    applications_name = applications.objects.get(id=applications_id).name
                    svn_path = applications.objects.get(id=applications_id).svn_path
                    deploy_version = int(str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")).lstrip("20"))
                    operator = applications.objects.get(id=applications_id).operator
                    latest_version = applications.objects.get(id=applications_id).version_id
                    if jenkins_select == '200':
                        p = deploy_history(business_id=business_id, business_name=business_name,
                                           applications_id=applications_id, applications_name=applications_name,
                                           release_version=release_version, release_reason=release_reason,
                                           latest_version=latest_version, applicant=username, deploy_version=deploy_version,
                                           operator=operator, remote_ip=remote_ip, svn_path=svn_path, war_path=war_path,
                                           status=status, email_address=email_address, jenkins_select=jenkins_select,
                                           type=app_type, war_name=war_name, date_added=date_added)
                        p.save()
                        time.sleep(10)
                        # jenkins_job
                        deploy_history.objects.filter(deploy_version=deploy_version).update(status="XK待测试")
                        smg = u"应用 %s 发布申请提交成功！已开始打版并自动发布到XK环境。。。" % applications_name
                        # return HttpResponse(smg)
                    else:
                        if war_path == "":
                            emg = u'不需要在线打包时，程序包位置不能为空！'
                        else:
                            p = deploy_history(business_id=business_id, business_name=business_name,
                                               applications_id=applications_id, applications_name=applications_name,
                                               release_version=release_version, release_reason=release_reason,
                                               latest_version=latest_version, applicant=username, deploy_version=deploy_version,
                                               operator=operator, remote_ip=remote_ip, svn_path=svn_path, war_path=war_path,
                                               status=status, email_address=email_address, jenkins_select=jenkins_select,
                                               type=app_type, war_name=war_name, date_added=date_added)
                            p.save()
                            # ansible_play(war_path)
                            # time.sleep(10)
                            deploy_history.objects.filter(deploy_version=deploy_version).update(status="XK待测试")
                            smg = u'应用 %s 发布申请提交成功！将自动发布至XK环境！' % applications_name
        except ServerError:
            pass

    return my_render('home_application/apply.html', locals(), request)

def business_get_apps(request):
    """
    根据business_id获取下面的应用列表
    """

def applylist(request):
    """
    申请列表
    """
    username = request.user.username
    admin_user = ['admin']
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    business_list = business_info.objects.all()
    if keyword:
        posts = deploy_history.objects.filter(Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(date_added__contains=keyword))
    else:
        if username in admin_user:
            posts = deploy_history.objects.all().order_by('-id')
        else:
            posts = deploy_history.objects.filter(applicant=username).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/applylist.html', locals(), request)

def apply_edit(request):
    """
    修改申请
    """
    apply_id = request.GET.get('id', '')
    business_list = business_info.objects.all()
    apply_select = deploy_history.objects.filter(id=apply_id)

    if request.method == 'POST':
        business_id = request.POST.get('business_select', '')
        business_name = business_info.objects.get(id=business_id).name
        applications_name = request.POST.get('name', '')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        release_version = request.POST.get('version_id')
        release_reason = request.POST.get('release_reason', '')
        # pre_release_time_str = request.POST.get('pre_release_time')
        # pre_release_time = pre_release_time_str.replace('&nbsp;', ' ')
        svn_path = request.POST.get('svn_path', '')
        email_address = request.POST.get('email_address_post', '')
        status = "XK待测试"
        app_type = request.POST.get('app_type', '')
        try:
            app_exist = applications.objects.filter(name=applications_name).count()
            if app_exist:
                applications_id = applications.objects.get(name=applications_name).id
                latest_version = applications.objects.get(id=applications_id).version_id
                deploy_history.objects.filter(id=apply_id).update(business_id=business_id, business_name=business_name, applications_id=applications_id, applications_name=applications_name,
                                                                  release_version=release_version, release_reason=release_reason, svn_path=svn_path, war_path=war_path, status=status,
                                                                  email_address=email_address, type=app_type, war_name=war_name)
                smg = u'应用 %s 申请修改成功！' % applications_name
                # return HttpResponse(smg)
            else:
                if applications_name == "":
                    emg = u'应用名称不能为空！'
                else:
                    emg = u'应用%s不存在,请先新建应用！' % applications_name
                    # return HttpResponse(emg)
        except ServerError as e:
            error = e.message
            emg = u'应用 %s 申请修改失败，错误：' % applications_name, error
            # return HttpResponse(emg)
        # return HttpResponseRedirect(reverse('home_application.views.apply_edit')+'?id=%s' % apply_id)

    return my_render('home_application/apply_edit.html', locals(), request)

def apply_info(request):
    """
    查看申请
    """
    apply_id = request.GET.get('id', '')
    business_list = business_info.objects.all()
    applications_list = applications.objects.all()
    apply_select = deploy_history.objects.filter(id=apply_id)
    # return HttpResponseRedirect(reverse('home_application.views.apply_edit')+'?id=%s' % apply_id)

    return my_render('home_application/apply_info.html', locals(), request)

def deploy_info(request):
    """
    查看发布日志
    """
    apply_id = request.GET.get('id', '')
    apply_select = deploy_history.objects.filter(id=apply_id)
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    jenkins_select = deploy_history.objects.get(id=apply_id).jenkins_select
    task_buildnum = get_jenkins_job_lastbuild_number(applications_name)  # jenkins_task_record.objects.get(task_id=apply_id).task_buildnum
    if jenkins_select == '200':
        smg = get_jenkins_jobs_output(applications_name, task_buildnum)
        # print smg
        return render_to_response('home_application/deploy_info.html', locals(), context_instance=RequestContext(request))
        # return HttpResponse(smg)
    else:
        os.system("scp root@10.10.18.240:/tmp/deploy_logs/XK_%s.log /var/log/devops/XK_%s.log" % (applications_name, applications_name))
        f = open(r'/var/logs/devop/XK_%s.log' % applications_name, 'r')
        try:
            resp = f.read()
        finally:
            f.close()
        return render_to_response('home_application/deploy_info.html', locals(), context_instance=RequestContext(request))
   # return my_render('home_application/apply_info.html', locals(), request)

def apply_del(request):
    """
    删除申请
    """
    apply_id = request.GET.get('id', '')
    if apply_id:
        deploy_history.objects.filter(id=apply_id).delete()
        smg = u'删除成功！'
    return HttpResponse(smg)

def testlist_xk(request):
    """
    XK待测试列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    test_keyword = "XK待测试"
    if keyword:
        posts = deploy_history.objects.filter(Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(applicant__contains=keyword)).filter(status__contains=test_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=test_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/testlist_xk.html', locals(), request)

def testlist_sc(request):
    """
    生产待测试列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    test_keyword = "生产待测试"
    if keyword:
        posts = deploy_history.objects.filter(Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(applicant__contains=keyword)).filter(status__contains=test_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=test_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/testlist_sc.html', locals(), request)

def test_pass_xk(request):
    """
    XK测试通过
    """
    username = request.user.username
    date_tested = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    # test_opinion = request.GET.get('test_opinion', '')
    status = "线上待发布"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, tester=username, date_tested=date_tested )
        deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                             pre_status=deploy_statuscode.DEPLOY_SECOND_STATUS,
                                             new_status=deploy_statuscode.DEPLOY_THIRD_STATUS,
                                             operator=username)
    return HttpResponse(u'线上待发布')

def test_pass_sc(request):
    """
    线上测试通过
    """
    username = request.user.username
    date_tested = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    # test_opinion = request.POST.get('test_opinion', '')
    status = "完成发布"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, tester=username, date_tested=date_tested)
        deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                             pre_status=deploy_statuscode.DEPLOY_FOURTH_STATUS,
                                             new_status=deploy_statuscode.DEPLOY_FIFTH_STATUS,
                                             operator=username)
    return HttpResponse(u'完成发布')

def test_back_xk(request):
    """
    XK测试退回
    """
    username = request.user.username
    date_tested = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    status = "XK测试退回"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, tester=username, date_tested=date_tested)
        deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                             pre_status=deploy_statuscode.DEPLOY_SECOND_STATUS,
                                             new_status=deploy_statuscode.TEST_XK_RETURN_STATUS,
                                             operator=username)

    return HttpResponse(u'XK测试退回')

def test_back_sc(request):
    """
    线上测试退回
    """
    username = request.user.username
    date_tested = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    status = "生产测试退回"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, tester=username, date_tested=date_tested)
        deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                             pre_status=deploy_statuscode.DEPLOY_FOURTH_STATUS,
                                             new_status=deploy_statuscode.TEST_SC_RETURN_STATUS,
                                             operator=username)
    return HttpResponse(u'生产测试退回')

def rollbacklist(request):
    """
    回滚列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    rollback_keyword = "回滚"
    if keyword:
        posts = deploy_history.objects.filter(
            Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(
                applicant__contains=keyword)).filter(status__contains=rollback_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=rollback_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/rollbacklist.html', locals(), request)

def returnedlist(request):
    """
    退回列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    return_keyword = "退回"
    if keyword:
        posts = deploy_history.objects.filter(
            Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(
                applicant__contains=keyword)).filter(status__contains=return_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=return_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/returnedlist.html', locals(), request)

def successlist(request):
    """
    退回列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    test_keyword = "完成发布"
    if keyword:
        posts = deploy_history.objects.filter(
            Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(
                applicant__contains=keyword)).filter(status__contains=test_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=test_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/successlist.html', locals(), request)

def review(request):
    """
    审核发布
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    review_keyword1 = "线上待发布"
    review_keyword2 = "生产发布中"
    review_keyword3 = "生产测试退回"
    if keyword:
        posts = deploy_history.objects.filter(Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(applicant__contains=keyword) | Q(status__contains=review_keyword1)| Q(status__contains=review_keyword2)| Q(status__contains=review_keyword3)).order_by('-id')
    else:
        posts = deploy_history.objects.filter(Q(status__contains=review_keyword1)| Q(status__contains=review_keyword2)| Q(status__contains=review_keyword3)).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/review.html', locals(), request)

def review_pass(request):
    """
    审核通过
    """
    username = request.user.username
    date_reviewed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    app_id = deploy_history.objects.get(id=apply_id).applications_id
    deploy_version_id = deploy_history.objects.get(id=apply_id).deploy_version

    if apply_id:
        war_path = deploy_history.objects.get(id=apply_id).war_path
        applications_name = deploy_history.objects.get(id=apply_id).applications_name
        deploy_history.objects.filter(id=apply_id).update(status=deploy_statuscode.DEPLOYING_SC_STATUS,
                                                          reviewer=username, date_reviewed=date_reviewed)
        if sc_deploy.delay(apply_id, war_path, applications_name):
            applications.objects.filter(id=app_id).update(version_id=deploy_version_id)
            deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                                 pre_status=deploy_statuscode.DEPLOY_THIRD_STATUS,
                                                 new_status=deploy_statuscode.DEPLOY_FOURTH_STATUS,
                                                 operator=username)
            logger.debug(u'应用' + applications_name + u'已发布至生产环境！')
        else:
            deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                                 pre_status=deploy_statuscode.DEPLOY_THIRD_STATUS,
                                                 new_status=deploy_statuscode.DEPLOY_FAILED_STATUS,
                                                 operator=username)
            logger.error(u'应用' + applications_name + u'发布生产失败！')

    return HttpResponse(u'生产待测试')

def review_back(request):
    """
    审核退回
    """
    username = request.user.username
    date_reviewed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    pre_status = deploy_history.objects.get(id=apply_id).status
    status = "审核退回"

    if apply_id:
        deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                             pre_status=pre_status,
                                             new_status=deploy_statuscode.REVIEW_BACK_STATUS,
                                             operator=username)
        deploy_history.objects.filter(id=apply_id).update(status=status, reviewer=username, date_reviewed=date_reviewed)

    return HttpResponse(u'审核退回')

def review_rollback(request):
    """
    回滚操作
    """
    username = request.user.username
    date_reviewed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_name = deploy_history.objects.get(id=apply_id).applications_name
    pre_status = deploy_history.objects.get(id=apply_id).status
    status = "已回滚"

    if apply_id:
        deploy_status_history.objects.create(task_id=apply_id, app_name=applications_name,
                                             pre_status=pre_status,
                                             new_status=deploy_statuscode.ROLLBACK_STATUS,
                                             operator=username)
        deploy_history.objects.filter(id=apply_id).update(status=status, reviewer=username, date_reviewed=date_reviewed)
    return HttpResponse(u'已回滚')

def package(request):
    """
    应用打包
    """
    return my_render('home_application/package.html', locals(), request)

def newapp(request):
    """
    新建应用
    """
    username = request.user.username
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    business_list = business_info.objects.all()
    if request.method == 'POST':
        business_id = request.POST.get('business_select', '')
        business_name = business_info.objects.get(id=business_id).name
        config_path = request.POST.get('config_path', '')
        name = request.POST.get('name')
        alias = request.POST.get('alias', '')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        svn_path = request.POST.get('svn_path', '')
        cluster_num = request.POST.get('cluster_num', '')
        master = request.POST.get('master', '')
        owner = request.POST.get('owner', '')
        operator = request.POST.get('operator', '')
        deploy_info_xk = request.POST.get('deploy_info_xk', '')
        deploy_info_sc = request.POST.get('deploy_info_sc', '')
        status = "新建"
        version_id = "0"
        version_name = request.POST.get('version_name', '')
        type = request.POST.get('type', '')

        try:
            app_exist = applications.objects.filter(name=name).count()
            if app_exist:
                emg = u'应用 %s 已存在！' % name
            else:
                if name == "":
                    emg = u'应用名称不能为空！'
                else:
                    xk_infos = deploy_info_xk.strip().split('\r\n')
                    sc_infos = deploy_info_xk.strip().split('\r\n')
                    a = ""
                    b = ""
                    for xk_info in xk_infos:
                        xk_ip = xk_info.split(':')[0]
                        a = a + ',' + xk_ip
                    for sc_info in sc_infos:
                        sc_ip = sc_info.split(':')[0]
                        b = b + ',' + sc_ip
                    target_ip_xk = a.lstrip(",")
                    target_ip_sc = b.lstrip(",")
                    p = applications(business_id=business_id, business_name=business_name, name=name, alias=alias, config_path=config_path,
                                     master=master, owner=owner, version_id=version_id, version_name=version_name, deploy_info_xk=deploy_info_xk,
                                     deploy_info_sc=deploy_info_sc, target_ip_xk=target_ip_xk, target_ip_sc=target_ip_sc,
                                     cluster_num=cluster_num,svn_path=svn_path, war_path=war_path, war_name=war_name,
                                     status=status, operator=operator, type=type, date_added=date_added)
                    p.save()
                    jsonData = TableToJson()
                    print (u'转换为json格式的数据：', jsonData)
                    # 以读写方式w+打开文件，路径前加r，防止字符转义
                    f = open(r'static/js/cityData.json', 'w+')
                    # 写数据
                    f.write(jsonData)
                    # 关闭文件
                    f.close()
                    smg = u"应用 %s 添加成功！" % name
        except ServerError:
            pass

    return my_render('home_application/newapp.html', locals(), request)

def applist(request):
    """
    应用列表
    """
    username = request.user.username
    posts = applications.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    if keyword:
        posts = applications.objects.filter(Q(name__contains=keyword) | Q(business_name__contains=keyword) | Q(target_server_ip__contains=keyword) | Q(version_id__contains=keyword) | Q(master__contains=keyword) | Q(owner__contains=keyword))
    else:
        posts = applications.objects.order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/applist.html', locals(), request)

def app_edit(request):
    """
    edit a apply data
    修改应用信息
    """
    app_id = request.GET.get('id', '')
    business_list = business_info.objects.all()
    app_select = applications.objects.filter(id=app_id)
    app_name = applications.objects.get(id=app_id).name
    svn_url = applications.objects.get(id=app_id).svn_path

    if request.method == 'POST':
        business_id = request.POST.get('business_select', '')
        business_name = business_info.objects.get(id=business_id).name
        config_path = request.POST.get('config_path', '')
        name = request.POST.get('name')
        alias = request.POST.get('alias', '')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        deploy_info_xk = request.POST.get('deploy_info_xk', '')
        deploy_info_sc = request.POST.get('deploy_info_sc', '')
        svn_path = request.POST.get('svn_path', '')
        cluster_num = request.POST.get('cluster_num', '')
        type = request.POST.get('type', '')
        master = request.POST.get('master', '')
        owner = request.POST.get('owner', '')
        operator = request.POST.get('operator', '')

        try:
            app_exist = applications.objects.filter(name=name).exclude(name=app_name).count()
            if app_exist:
                emg = u'应用 %s 已存在！' % name
                # raise ServerError(emg)
            else:
                if name == "":
                    emg = u'应用名称不能为空！'
                else:
                    xk_infos = deploy_info_xk.strip().split('\r\n')
                    sc_infos = deploy_info_xk.strip().split('\r\n')
                    a = ""
                    b = ""
                    for xk_info in xk_infos:
                        xk_ip = xk_info.split(':')[0]
                        a = a + ',' + xk_ip
                    for sc_info in sc_infos:
                        sc_ip = sc_info.split(':')[0]
                        b = b + ',' + sc_ip
                    target_ip_xk = a.lstrip(",")
                    target_ip_sc = b.lstrip(",")
                    applications.objects.filter(id=app_id).update(business_id=business_id, business_name=business_name, name=name, alias=alias, config_path=config_path,
                                                                  master=master, owner=owner, deploy_info_xk=deploy_info_xk, target_ip_xk=target_ip_xk, deploy_info_sc=deploy_info_sc,
                                                                  target_ip_sc=target_ip_sc, cluster_num=cluster_num, svn_path=svn_path, war_path=war_path, war_name=war_name,
                                                                  operator=operator, type=type)
                    smg = u'应用 %s 修改成功！' % name
                    jsonData = TableToJson()
                    print (u'转换为json格式的数据：', jsonData)
                    # 以读写方式w+打开文件，路径前加r，防止字符转义
                    f = open(r'static/js/cityData.json', 'w+')
                    # 写数据
                    f.write(jsonData)
                    # 关闭文件
                    f.close()
        except ServerError as e:
            error = e.message
            emg = u'应用 %s 修改失败！' % name
        #return HttpResponseRedirect(reverse('home_application.views.app_edit')+'?id=%s' % app_id)

    return my_render('home_application/app_edit.html', locals(), request)

def app_del(request):
    """
    删除应用
    """
    app_id = request.GET.get('id', '')
    if app_id:
        applications.objects.filter(id=app_id).delete()

    return HttpResponse(u'删除成功')

def appoperation(request):
    """
    应用操作
    """
    username = request.user.username
    posts = applications.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    if keyword:
        posts = applications.objects.filter(
            Q(name__contains=keyword) | Q(business_name__contains=keyword) | Q(target_server_ip__contains=keyword) | Q(version_id__contains=keyword) | Q(owner__contains=keyword))
    else:
        posts = applications.objects.order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/appoperation.html', locals(), request)

def monitor(request):
    """
    监控大盘展示
    """
    ss=250 #定义一个变量赋值，然后在界面中展示

    errorcount=get_error()[0] #定义一个变量赋值，然后在界面中展示
    urlslow=get_urlslow()[0]

    result = get_table('10.32.144.182', 'root', 'tongze@2011', 3306)
    # print '1', result
    # for s in result:
    #     print s
    return render_to_response('home_application/monitor.html', locals(), context_instance=RequestContext(request))

def urllist(request):
    """
    url检测速度
    """
    urldb = get_urllist('10.32.145.112', 'root', 'bk@321', 3306)
    # print '1', urldb
    # for s in urldb:
    #     print s
    return render_to_response('home_application/urllist.html', locals(), context_instance=RequestContext(request))


def elk(request):
    """
    日志系统
    """
    return render_mako_context(request, '/home_application/elk.html')

def get_all():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM apache_count WHERE note= 'ALL' ORDER BY time DESC LIMIT 1 "
        cur.execute(sql)
        allcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return allcount
def get_nb():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM apache_count WHERE note= 'nb' ORDER BY time DESC LIMIT 1 "
        cur.execute(sql)
        nbcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return nbcount

def get_ycyl():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM apache_count WHERE note= 'ycyl' ORDER BY time DESC LIMIT 1 "
        cur.execute(sql)
        ycylcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return ycylcount

def get_procount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' "
        cur.execute(sql)
        procount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return procount
def get_xkcount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '5' "
        cur.execute(sql)
        xkcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return xkcount

def get_jccount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '4' "
        cur.execute(sql)
        jccount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return jccount

def get_zbcount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '7' "
        cur.execute(sql)
        zbcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return zbcount

def get_proappcount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(*) FROM cc_ModuleBase WHERE ApplicationID = '6' AND SetID != 38"
        cur.execute(sql)
        proappcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return proappcount

def get_xkappcount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(*) FROM cc_ModuleBase WHERE ApplicationID = '5' AND SetID != 24"
        cur.execute(sql)
        xkappcount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return xkappcount
def get_zcptccount():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 37"
        cur.execute(sql)
        zcptccount = cur.fetchall()[0]
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return zcptccount


def get_zcptczj():
    try:
        conn = MySQLdb.connect(host='10.3.54.189', user='root', passwd='bk@321', db="cmdb",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 37"
        cur.execute(sql)
        zcptczj = cur.fetchall()[0]
        cur.close()

        cur1 = conn.cursor()
        sql1 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 39"
        cur1.execute(sql1)
        zsyyy = cur1.fetchall()[0]
        cur1.close()

        cur2 = conn.cursor()
        sql2 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 39"
        cur2.execute(sql2)
        zsyyyzj = cur2.fetchall()[0]
        cur2.close()

        cur3 = conn.cursor()
        sql3 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 40"
        cur3.execute(sql3)
        clhis = cur3.fetchall()[0]
        cur3.close()

        cur4 = conn.cursor()
        sql4 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 40"
        cur4.execute(sql4)
        clhiszj = cur4.fetchall()[0]
        cur4.close()

        cur5 = conn.cursor()
        sql5 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 41"
        cur5.execute(sql5)
        csyyy = cur5.fetchall()[0]
        cur5.close()

        cur6 = conn.cursor()
        sql6 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 41"
        cur6.execute(sql6)
        csyyyzj = cur6.fetchall()[0]
        cur6.close()

        cur7 = conn.cursor()
        sql7 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 42"
        cur7.execute(sql7)
        jgzx = cur7.fetchall()[0]
        cur7.close()

        cur8 = conn.cursor()
        sql8 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 42"
        cur8.execute(sql8)
        jgzxzj = cur8.fetchall()[0]
        cur8.close()

        cur9 = conn.cursor()
        sql9 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 44"
        cur9.execute(sql9)
        ylhl = cur9.fetchall()[0]
        cur9.close()

        cur10 = conn.cursor()
        sql10 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 44"
        cur10.execute(sql10)
        ylhlzj = cur10.fetchall()[0]
        cur10.close()

        cur11 = conn.cursor()
        sql11 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 45"
        cur11.execute(sql11)
        ycxd = cur11.fetchall()[0]
        cur11.close()

        cur12 = conn.cursor()
        sql12 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 45"
        cur12.execute(sql12)
        ycxdzj = cur12.fetchall()[0]
        cur12.close()

        cur13 = conn.cursor()
        sql13 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 46"
        cur13.execute(sql13)
        jkcs = cur13.fetchall()[0]
        cur13.close()

        cur14 = conn.cursor()
        sql14 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 46"
        cur14.execute(sql14)
        jkcszj = cur14.fetchall()[0]
        cur14.close()

        cur15 = conn.cursor()
        sql15 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 47"
        cur15.execute(sql15)
        ikeep = cur15.fetchall()[0]
        cur15.close()

        cur16 = conn.cursor()
        sql16 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 47"
        cur16.execute(sql16)
        ikeepzj = cur16.fetchall()[0]
        cur16.close()

        cur17 = conn.cursor()
        sql17 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 48"
        cur17.execute(sql17)
        isleep = cur17.fetchall()[0]
        cur17.close()

        cur18 = conn.cursor()
        sql18 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 48"
        cur18.execute(sql18)
        isleepzj = cur18.fetchall()[0]
        cur18.close()

        cur19 = conn.cursor()
        sql19 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 49"
        cur19.execute(sql19)
        xkw = cur19.fetchall()[0]
        cur19.close()

        cur20 = conn.cursor()
        sql20 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 49"
        cur20.execute(sql20)
        xkwzj = cur20.fetchall()[0]
        cur20.close()

        cur21 = conn.cursor()
        sql21 = "SELECT count(*) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 50"
        cur21.execute(sql21)
        qita = cur21.fetchall()[0]
        cur21.close()

        cur22 = conn.cursor()
        sql22 = "SELECT count(DISTINCT HostID) FROM cc_ModuleHostConfig WHERE ApplicationID = '6' AND SetID = 50"
        cur22.execute(sql22)
        qitazj = cur22.fetchall()[0]
        cur22.close()

        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return zcptczj,zsyyy,zsyyyzj,clhis,clhiszj,csyyy,csyyyzj,jgzx,jgzxzj,ylhl,ylhlzj,ycxd,ycxdzj,jkcs,jkcszj,ikeep,ikeepzj,isleep,isleepzj,xkw,xkwzj,qita,qitazj

def logstatus(request):
    ss = 250  # 定义一个变量赋值，然后在界面中展示
    allcount=get_all()[0] #定义一个变量赋值，然后在界面中展示
    ipcount=get_all()[1]
    nbcount=get_nb()[0] #从get_nb函数中获取宁波的访问量数据
    nbipcount=get_nb()[1]
    ycylcount=get_ycyl()[0] #从get_nb函数中获取宁波的访问量数据
    ycylipcount=get_ycyl()[1]
    procount=get_procount()[0]
    xkcount=get_xkcount()[0]
    jccount=get_jccount()[0]
    zbcount=get_zbcount()[0]
    proappcount=get_proappcount()[0]
    xkappcount = get_xkappcount()[0]
    allcount1=xkcount+jccount+procount+zbcount+5
    zcptccount=get_zcptccount()[0]
    zcptczj=get_zcptczj()[0][0]
    zsyyy=get_zcptczj()[1][0]
    zsyyyzj=get_zcptczj()[2][0]
    clhis=get_zcptczj()[3][0]
    clhiszj=get_zcptczj()[4][0]
    csyyy=get_zcptczj()[5][0]
    csyyyzj=get_zcptczj()[6][0]
    jgzx=get_zcptczj()[7][0]
    jgzxzj=get_zcptczj()[8][0]
    ylhl=get_zcptczj()[9][0]
    ylhlzj=get_zcptczj()[10][0]
    ycxd=get_zcptczj()[11][0]
    ycxdzj=get_zcptczj()[12][0]
    jkcs=get_zcptczj()[13][0]
    jkcszj=get_zcptczj()[14][0]
    ikeep=get_zcptczj()[15][0]
    ikeepzj=get_zcptczj()[16][0]
    isleep=get_zcptczj()[17][0]
    isleepzj=get_zcptczj()[18][0]
    xkw=get_zcptczj()[19][0]
    xkwzj=get_zcptczj()[20][0]
    qita=get_zcptczj()[21][0]
    qitazj=get_zcptczj()[22][0]
    hygeaipall=get_hygeaipall()
    apphybrid=get_apphybridipall()
    loadstatus=get_loadstatus()
    loadstatushis=get_loadstatushis()
    loadstatushmboss=get_loadstatushmboss()
    loadstatusycyl = get_loadstatusycyl()
    ycylipall = get_ycylipall()

    #print loadstatus

    #hygeadate=[]
    # for i in hygeaipall1:
    #     hygeaipall.append(int(str(i[2])))
    # for u in hygeaipall1:
    #     hygeadate.append(str(u[0]))

    return render_to_response('home_application/logstash.html', locals(), context_instance=RequestContext(request))


def get_hygeaipall():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()

        #sql = "SELECT t.Person_PHR_Code, t.Person_Name, t.Birthday, t.Gender_Name, t.Person_Nickname,  t.Name_Spell, t.Change_Time FROM acornhc_healthdata.phr_person_basic_info t limit 10"

        sql = "select DATE_FORMAT(time,'%y-%m-%d') as stat_date,note,max(ip) as cnt,pv from apache_count where note='hygea' group by DATE_FORMAT(time,'%y-%m-%d'),note ORDER BY stat_date DESC LIMIT 7 "
        cur.execute(sql)
        hygeaipall = cur.fetchall()

        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e
    except Exception, e1:
        print e1
    return hygeaipall

def get_apphybridipall():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()

        #sql = "SELECT t.Person_PHR_Code, t.Person_Name, t.Birthday, t.Gender_Name, t.Person_Nickname,  t.Name_Spell, t.Change_Time FROM acornhc_healthdata.phr_person_basic_info t limit 10"

        sql = "select DATE_FORMAT(time,'%y-%m-%d') as stat_date,note,max(ip) as cnt,pv from apache_count where note='apphybrid' group by DATE_FORMAT(time,'%y-%m-%d'),note ORDER BY stat_date DESC LIMIT 7 "
        cur.execute(sql)
        apphybrid = cur.fetchall()

        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e
    except Exception, e1:
        print e1
    return apphybrid

def get_loadstatus():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM load_status WHERE other='zsyyy' ORDER BY time DESC LIMIT 5 "
        cur.execute(sql)
        loadstatus = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return loadstatus

def get_loadstatushis():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM load_status WHERE other= 'his' ORDER BY time DESC LIMIT 2 "
        cur.execute(sql)
        loadstatushis = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return loadstatushis

def get_loadstatushmboss():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM load_status WHERE other= 'hmboss' ORDER BY time DESC LIMIT 2 "
        cur.execute(sql)
        loadstatushmboss = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return loadstatushmboss

def get_ycylipall():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()

        #sql = "SELECT t.Person_PHR_Code, t.Person_Name, t.Birthday, t.Gender_Name, t.Person_Nickname,  t.Name_Spell, t.Change_Time FROM acornhc_healthdata.phr_person_basic_info t limit 10"

        sql = "select DATE_FORMAT(time,'%y-%m-%d') as stat_date,note,max(ip) as cnt,max(pv) from apache_count where note='ycyl' group by DATE_FORMAT(time,'%y-%m-%d'),note ORDER BY stat_date DESC LIMIT 7 "
        cur.execute(sql)
        ycylipall = cur.fetchall()

        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e
    except Exception, e1:
        print e1
    return ycylipall
def get_loadstatusycyl():
    try:
        conn = MySQLdb.connect(host='10.32.145.112', user='root', passwd='bk@321', db="devops",
                               connect_timeout=10, port=int(3306), charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM load_status WHERE other= 'ycylweb' ORDER BY time DESC LIMIT 5 "
        cur.execute(sql)
        loadstatusycyl = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        pass
    except Exception, e1:
        print e1
    return loadstatusycyl