# -*- coding: utf-8 -*-

from common.mymako import render_mako_context


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
    新版首页-王有为
    """
    return render_mako_context(request, '/home_application/index.html')

def apply(request):
    """
    新版首页-王有为
    """
    return render_mako_context(request, '/home_application/apply.html')

def applylist(request):
    """
    新版首页-王有为
    """
    return render_mako_context(request, '/home_application/applylist.html')