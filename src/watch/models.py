#encoding=utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Asset(models.Model):
    sn = models.CharField(max_length=50,null=False)
    mac = models.CharField(max_length=50,null=False)
    type = models.CharField(max_length=50,null=False)
    hbversion = models.CharField(max_length=50,null=False)
    portalversion = models.CharField(max_length=50,null=False)
    create_date = models.DateTimeField(auto_now_add=True,null=False)
    update_date = models.DateTimeField(auto_now=True,null=False)
    
    #默认状态打印asset对象返回Asset Object
    #此处可以定制
    def __unicode__(self):
        #return label
        return self.sn
    