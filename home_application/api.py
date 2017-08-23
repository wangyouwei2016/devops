# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template import RequestContext
from django.shortcuts import render_to_response
from home_application.models import applications
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
import datetime
import subprocess
from home_application.models import deploy_history

def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page + 1)

def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """
    paginator = Paginator(post_objects, 10)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end

def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))

class ServerError(Exception):
    """
    self define exception
    自定义异常
    """
    pass

def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object

def db_add_applications(**kwargs):
    """
    add a app_deploy in database
    数据库中添加申请发布信息
    """
    name = kwargs.get('name')

    if not name:
        a_d = applications(**kwargs)
        a_d.save()

def ssh_xk_deploy(task_id, war_path, appname):
    try:
        a = os.system("ssh root@10.10.18.240 'sh /root/hubot_scripts/hubot_deploy_xk.sh %s %s'" % (war_path, appname))
        if not a:
            deploy_history.objects.filter(id=task_id).update(status="XK待测试")
            print u"XK发布成功！" + war_path
            return True
        else:
            deploy_history.objects.filter(id=task_id).update(status="发布失败")
            print u"XK发布失败！" + war_path
            return False
    except:
        deploy_history.objects.filter(id=task_id).update(status="发布失败")
        print u"系统异常，XK发布失败！" + war_path
        return False

def ssh_sc_deploy(task_id, war_path, appname):
    try:
        if war_path:
            deploy_date = war_path.split('/')[2]
            Formal_war_path = war_path.replace('XK', 'Formal')
            os.system("ssh root@10.10.18.240 'mkdir -p /warehouse/to_deploy/%s/Formal/%s'" % (appname, deploy_date))
            os.system("ssh root@10.10.18.240 'cp /warehouse/to_deploy/%s /warehouse/to_deploy/%s'" % (war_path, Formal_war_path))
            a = os.system("ssh root@10.10.18.240 'sh /root/hubot_scripts/hubot_deploy_sc.sh %s %s'" % (Formal_war_path, appname))
            if not a:
                deploy_history.objects.filter(id=task_id).update(status="生产待测试")
                print u"生产发布成功！" + Formal_war_path
                return True
            else:
                deploy_history.objects.filter(id=task_id).update(status="发布失败")
                print u"生产发布失败！" + Formal_war_path
                return False
        else:
            deploy_history.objects.filter(id=task_id).update(status="生产待测试")
            print u"这是通过Jenkins打版的。"
            return True
    except:
        return False
