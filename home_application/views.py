# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_mako,render_json
import MySQLdb
from account.models import BkUser
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from home_application.models import applications, business_info, deploy_history, status_info, business_applications, applications_config, applications_config_item
from home_application.api import pages, my_render, ServerError, get_object,db_add_applications
from django.shortcuts import render
import datetime
import time
from django.template.context_processors import csrf

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

def apply(request):
    """
    发布申请
    """
    username = request.user.username
    user_email = BkUser.objects.get(username=username).email
    remote_ip = request.META.get('REMOTE_ADDR')
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    business_list = business_info.objects.all()
    business_select = request.GET.get('business_select', '')
    applications_list = applications.objects.filter(business_id=business_select)

    if request.method == 'POST':
        business_id = request.POST.get('business_select', '')
        business_name = business_info.objects.get(id=business_id).name
        applications_name = request.POST.get('name', '')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        release_version = request.POST.get('version_id')
        release_reason = request.POST.get('release_reason', '')
        pre_release_time_str = request.POST.get('pre_release_time')
        pre_release_time = pre_release_time_str.replace('&nbsp;', ' ')
        svn_path = request.POST.get('svn_path', '')
        email_address_post = request.POST.get('email_address_post', '')
        email_address = user_email + ',' + email_address_post
        status = "XK待测试"
        app_type = request.POST.get('app_type', '')

        try:
            app_exist = applications.objects.filter(name=applications_name).count()
            if app_exist:
                applications_id = applications.objects.get(name=applications_name).id
                operator = applications.objects.get(name=applications_name).operator
                latest_version = applications.objects.get(id=applications_id).version_id
                p = deploy_history(business_id=business_id, business_name=business_name,
                                   applications_id=applications_id, applications_name=applications_name,
                                   release_version=release_version, release_reason=release_reason,
                                   latest_version=latest_version, applicant=username,
                                   operator=operator, remote_ip=remote_ip, svn_path=svn_path, war_path=war_path,
                                   status=status, email_address=email_address,
                                   type=app_type, war_name=war_name, date_added=date_added,
                                   pre_release_time=pre_release_time)
                p.save()
                # applications.objects.filter(id=applications_id).update(version_id=release_version)
                smg = u"应用 %s 发布申请提交成功！" % applications_name
                # return HttpResponse(smg)
            else:
                if applications_name == "":
                    emg = u'应用名称不能为空！'
                else:
                    emg = u'应用%s不存在,请先新建应用！' % applications_name
                    # return HttpResponse(emg)
        except ServerError:
            pass

    return my_render('home_application/apply.html', locals(), request)

def applylist(request):
    """
    申请列表
    """
    username = request.user.username
    admin_user = ['admin']
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
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
        pre_release_time_str = request.POST.get('pre_release_time')
        pre_release_time = pre_release_time_str.replace('&nbsp;', ' ')
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
                                                                  email_address=email_address, type=app_type, war_name=war_name, pre_release_time=pre_release_time)
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

def apply_del(request):
    """
    删除申请
    """
    apply_id = request.GET.get('id', '')
    if apply_id:
        deploy_history.objects.filter(id=apply_id).delete()
        smg = u'删除成功！'
    return HttpResponse(smg)

def testlist(request):
    """
    待测试列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    test_keyword_xk = "XK待测试"
    test_keyword_sc = "生产待测试"
    if keyword:
        posts1 = deploy_history.objects.filter(Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(applicant__contains=keyword)).filter(status__contains=test_keyword_xk).order_by('-id')
        posts2 = deploy_history.objects.filter(
            Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(
                applicant__contains=keyword)).filter(status__contains=test_keyword_sc).order_by('-id')
    else:
        posts1 = deploy_history.objects.filter(status__contains=test_keyword_xk).order_by('-id')
        posts2 = deploy_history.objects.filter(status__contains=test_keyword_sc).order_by('-id')
    contact_list, p, contacts1, page_range, current_page, show_first, show_end = pages(posts1, request)
    contact_list, p, contacts2, page_range, current_page, show_first, show_end = pages(posts2, request)
    return my_render('home_application/testlist.html', locals(), request)

def test_pass(request):
    """
    测试通过
    """
    username = request.user.username
    date_tested = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    status = "测试通过"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, tester=username, date_tested=date_tested)

    return HttpResponse(u'测试通过')

def test_back(request):
    """
    测试退回
    """
    username = request.user.username
    date_tested = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    status = "测试退回"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, tester=username, date_tested=date_tested)

    return HttpResponse(u'测试退回')

def rollbacklist(request):
    """
    回滚列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    test_keyword = "回滚"
    if keyword:
        posts = deploy_history.objects.filter(
            Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(
                applicant__contains=keyword)).filter(status__contains=test_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=test_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/rollbacklist.html', locals(), request)

def returnedlist(request):
    """
    退回列表
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    test_keyword = "退回"
    if keyword:
        posts = deploy_history.objects.filter(
            Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(
                applicant__contains=keyword)).filter(status__contains=test_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=test_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/returnedlist.html', locals(), request)

def review(request):
    """
    审核发布
    """
    username = request.user.username
    posts = deploy_history.objects.all().order_by('-id')
    keyword = request.GET.get('keyword', '')
    review_keyword = "测试通过"
    if keyword:
        posts = deploy_history.objects.filter(Q(applications_name__contains=keyword) | Q(business_name__contains=keyword) | Q(applicant__contains=keyword)).filter(status__contains=review_keyword).order_by('-id')
    else:
        posts = deploy_history.objects.filter(status__contains=review_keyword).order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('home_application/review.html', locals(), request)

def review_pass(request):
    """
    审核通过
    """
    username = request.user.username
    date_reviewed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    applications_id = deploy_history.objects.get(id=apply_id).applications_id
    release_version = deploy_history.objects.get(id=apply_id).release_version
    status = "生产待测试"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, reviewer=username, date_reviewed=date_reviewed)
        applications.objects.filter(id=applications_id).update(version_id=release_version)

    return HttpResponse(u'审核通过')

def review_back(request):
    """
    审核退回
    """
    username = request.user.username
    date_reviewed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apply_id = request.GET.get('id', '')
    status = "审核退回"

    if apply_id:
        deploy_history.objects.filter(id=apply_id).update(status=status, reviewer=username, date_reviewed=date_reviewed)

    return HttpResponse(u'审核退回')

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
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        target_server_ip = request.POST.get('target_server_ip', '')
        deploy_path = request.POST.get('deploy_path', '')
        svn_path = request.POST.get('svn_path', '')
        cluster_num = request.POST.get('cluster_num', '')
        master = request.POST.get('master', '')
        owner = request.POST.get('owner', '')
        operator = request.POST.get('operator', '')
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
                    p = applications(business_id=business_id, business_name=business_name, name=name, config_path=config_path, master=master, owner=owner,
                                     version_id=version_id, version_name=version_name, target_server_ip=target_server_ip, cluster_num=cluster_num,
                                     deploy_path=deploy_path, svn_path=svn_path, war_path=war_path, war_name=war_name, status=status, operator=operator,
                                     type=type, date_added=date_added)
                    p.save()
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

    if request.method == 'POST':
        business_id = request.POST.get('business_select', '')
        business_name = business_info.objects.get(id=business_id).name
        config_path = request.POST.get('config_path', '')
        name = request.POST.get('name')
        war_path = request.POST.get('war_path', '')
        war_name = war_path.split('/')[-1]
        target_server_ip = request.POST.get('target_server_ip', '')
        deploy_path = request.POST.get('deploy_path', '')
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
                    applications.objects.filter(id=app_id).update(business_id=business_id, business_name=business_name, name=name, config_path=config_path,
                                                                  master=master, owner=owner, target_server_ip=target_server_ip, cluster_num=cluster_num,
                                                                  deploy_path=deploy_path, svn_path=svn_path, war_path=war_path, war_name=war_name,
                                                                  operator=operator, type=type)
                    smg = u'应用 %s 修改成功！' % name
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