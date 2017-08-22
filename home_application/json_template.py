# -*- coding: utf-8 -*-
from home_application.models import deploy_history

def json_template_base_business(business_counts1,business_counts2,business_counts3,business_counts4,business_counts5,business_counts6,business_counts7,business_counts8,business_counts9,business_counts10,business_counts11,business_counts12):
    template_base_business = u'''
{
    "code": 0,
    "result": true,
    "messge": "success",
    "data": {
        "title": "",
        "series": [{
            "value": %s,
            "name": "掌上云医院"
        }, {
            "value": %s,
            "name": "城市云医院"
        }, {
            "value": %s,
            "name": "养老护理"
        }, {
            "value": %s,
            "name": "健管"
        }, {
            "value": %s,
            "name": "远程心电"
        }, {
            "value": %s,
            "name": "云HIS"
        }, {
            "value": %s,
            "name": "IKEEPER"
        }, {
            "value": %s,
            "name": "支撑平台"
        }, {
            "value": %s,
            "name": "熙康网"
        }, {
            "value": %s,
            "name": "ISLEEP"
        }, {
            "value": %s,
            "name": "健康城市"
        }, {
            "value": %s,
            "name": "其他"
        }
        ]
    }
}''' % (business_counts1,business_counts2,business_counts3,business_counts4,business_counts5,business_counts6,business_counts7,business_counts8,business_counts9,business_counts10,business_counts11,business_counts12)
    f = open(r'static/js/json_template_base_business.json', 'w+')
    # 写数据
    f.write(template_base_business)
    # 关闭文件
    f.close()

def json_template_base_month(all_month_counts,success_month_counts):
    template_base_month = u'''
{
    "code": 0,
    "result": true,
    "messge": "success",
    "data": {
        "xAxis": [{
            "type": "category",
            "data": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        }],
        "series": [{
            "name": "发布量",
            "type": "bar",
            "data": %s
        }, {
            "name": "成功量",
            "type": "bar",
            "data": %s
        }]
    }

}''' % (all_month_counts, success_month_counts)
    f = open(r'static/js/json_template_base_month.json', 'w+')
    # 写数据
    f.write(template_base_month)
    # 关闭文件
    f.close()

