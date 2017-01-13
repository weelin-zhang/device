#encoding=utf8
import json
from django.shortcuts import render,HttpResponse,render_to_response
from models import Asset
# Create your views here.

from plugins.tool import is_status_timeout,separate_items

from plugins.common import try_int,page_info,get_html_pages


def handler(request):

    if request.method != 'POST':
        return HttpResponse('fuck')
    
    data = request.POST
    
    sn, mac, type, hbversion, portalversion = data['sn'], data['mac'], data['type'], data['hbversion'], data['portalversion'] 
    
    obj = Asset.objects.filter(sn=sn)
    if obj:#存在
        print '存在'
        obj[0].hbversion = hbversion
        obj[0].portalversion = portalversion
        obj[0].save()
    else:   
        Asset.objects.create(sn=sn, mac=mac, type=type, hbversion=hbversion, portalversion=portalversion)
    
    return HttpResponse('ok')


def getinfo(request):
    
    ret ={'assets':[],'count':0,'pages_html':[]}
    key, status = request.POST.get('keyWord'), request.POST.get('status')
    if request.method == 'POST':
        if key:
            objs_by_key = Asset.objects.filter(sn__icontains=key.strip()) 
            if status == 'Online':
                objs_by_key_on_off = separate_items(objs_by_key, 'on')
            elif status == 'Offline':
                objs_by_key_on_off = separate_items(objs_by_key, 'off')
            else:
                objs_by_key_on_off = separate_items(objs_by_key)
            ret['key'] = key.strip()
            ret['assets'] = objs_by_key_on_off
            ret['count'] = len(objs_by_key_on_off)
            
            return render(request, 'watch/index.html',ret)
            
        elif not key:
            objs = Asset.objects.order_by('-update_date')
            if status == 'Online':
                objs_by_key_on_off = separate_items(objs, 'on')
            elif status == 'Offline':
                objs_by_key_on_off = separate_items(objs, 'off')
            else:
                objs_by_key_on_off = separate_items(objs)
            ret['key'] = ''
            ret['assets'] = objs_by_key_on_off    
            ret['count'] = len(objs_by_key_on_off)   
            return render(request, 'watch/index.html',ret)
        
    assets = Asset.objects.filter().order_by('-update_date')#time 大-->>--小
    ret['assets'] = assets
    ret['count'] = len(assets)
    return render(request, 'watch/index.html',ret)



def info(request,page):
    page = try_int(page, 1)
    ret ={'assets':[],'count':0,'pages_html':[]}
    #获取cookie    
    key_from_cookie = request.COOKIES.get('key','')
    status_from_cookie = request.COOKIES.get('status','all')
    if key_from_cookie:
        objs_by_key = Asset.objects.filter(sn__icontains=key_from_cookie.strip()) 
        if status_from_cookie == 'Online':
            objs = separate_items(objs_by_key, 'on')
        elif status_from_cookie == 'Offline':
            objs = separate_items(objs_by_key, 'off')
        else:
            objs = separate_items(objs_by_key)
            
    elif not key_from_cookie:
        print 2
        all_objs = Asset.objects.order_by('-update_date')
        if status_from_cookie == 'Online':
            objs = separate_items(all_objs, 'on')
        elif status_from_cookie == 'Offline':
            objs = separate_items(all_objs, 'off')
        else:
            objs = separate_items(all_objs)
    
    #page_info 对象
    pageobj = page_info(len(objs),page,10)
    ret['assets'] = objs[pageobj.start:pageobj.end] 
    ret['count'] = len(objs)
    page_html_l = get_html_pages(page, pageobj.max_pageNum, 3)
    ret['pages_html'] = page_html_l
    return render(request, 'watch/index.html',ret)
        
