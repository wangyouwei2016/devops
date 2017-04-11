# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
import MySQLdb
from django.shortcuts import render_to_response
from django.template import RequestContext

def compute(request):

    result = get_table('10.32.144.182', 'root', 'tongze@2011', 3306)
    print '1',result
    for s in result:
        print s
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
    return render_mako_context(request, '/home_application/index.html')

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

def monitor(request):
    """
    监控大盘展示
    """
    result = get_table('10.32.144.182', 'root', 'tongze@2011', 3306)
    print '1',result
    for s in result:
        print s
    return render_to_response('home_application/monitor.html', locals(), context_instance=RequestContext(request))
