# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
import MySQLdb
from django.shortcuts import render_to_response
from django.template import RequestContext



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
    print '1',result
    for s in result:
        print s
    return render_to_response('home_application/index.html', locals(), context_instance=RequestContext(request))

def apply(request):
    """
    发布申请
    """
    return render_mako_context(request, '/home_application/apply.html')

def applylist(request):
    """
    发布列表
    """
    return render_mako_context(request, '/home_application/applylist.html')

def operation(request):
    """
    发布列表
    """
    return render_mako_context(request, '/home_application/operation.html')

def urllist(request):
    """
    发布列表
    """
    urldb = get_urllist('10.32.145.112', 'root', 'bk@321', 3306)
    print '1',urldb
    for s in urldb:
        print s
    return render_to_response('home_application/urllist.html', locals(), context_instance=RequestContext(request))


def elk(request):
    """
    发布列表
    """
    return render_mako_context(request, '/home_application/elk.html')
def monitor(request):
    """
    监控大盘展示
    """
    errorcount=get_error()[0] #定义一个变量赋值，然后在界面中展示
    urlslow=get_urlslow()[0]

    result = get_table('10.32.144.182', 'root', 'tongze@2011', 3306)
    print '1',result
    for s in result:
        print s
    return render_to_response('home_application/monitor.html', locals(), context_instance=RequestContext(request))

def menu(request):
    """
    菜单列表
    """
    return render_mako_context(request, '/home_application/menu.html')


def testlist(request):
    """
    待测试列表
    """
    return render_mako_context(request, '/home_application/testlist.html')

def rollbacklist(request):
    """
    回滚列表
    """
    return render_mako_context(request, '/home_application/rollbacklist.html')

def returnedlist(request):
    """
    退回列表
    """
    return render_mako_context(request, '/home_application/returnedlist.html')

def review(request):
    """
    审核发布
    """
    return render_mako_context(request, '/home_application/review.html')

def package(request):
    """
    应用打包
    """
    return render_mako_context(request, '/home_application/package.html')

def newapp(request):
    """
    新建应用
    """
    return render_mako_context(request, '/home_application/newapp.html')

def applist(request):
    """
    应用列表
    """
    return render_mako_context(request, '/home_application/applist.html')

def appoperation(request):
    """
    应用操作
    """
    return render_mako_context(request, '/home_application/appoperation.html')