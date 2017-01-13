#_*_coding:utf-8_*_
'''
Created on 2016年12月3日

@author: weelin
'''

from django.utils.safestring import mark_safe


def try_int(arg,default):
    try:
        arg = int(arg)
    except:
        arg=default
    return arg




#定义分页类

class page_info(object):
    
    def __init__(self,allcount,curpage,per_item):
        self.__AllCount = allcount
        self.__CurPage = curpage
        self.__PerItems = per_item
        
        
        
    @property
    def start(self):
        
        return (self.__CurPage-1)*self.__PerItems
        
    @property    
    def end(self):
        if self.__CurPage*self.__PerItems>self.__AllCount:
            return self.__AllCount
        return self.__CurPage*self.__PerItems
    
    
    
    @property
    
    def max_pageNum(self):
        maxNum = (self.__AllCount+self.__PerItems-1)/self.__PerItems 
        return maxNum  
        
def get_html_pages(curpage,max_page,marginnum):
    
    '''
    curpage--当前显示页
    
    max_page--总页数
    
    marginnum--当前页左右显示的页码marginnum-1
    
    '''
    
    page_html_l = []
    print 'max_page:',max_page
    #设置上一页、下一页
    if curpage == 1:
        pre_html = mark_safe('<a>上一页</a>')
        if curpage == max_page:
            next_html = mark_safe('<a>下一页</a>')
        else:
            next_html = mark_safe("<a href='/watch/info/%s'>%s</a>" %(curpage+1,'下一页'))
    elif curpage==max_page:
        pre_html = mark_safe("<a href='/watch/info/%s'>%s</a>" %(curpage-1,'上一页'))
        next_html = mark_safe('<a>下一页</a>')
    else:
        pre_html = mark_safe("<a href='/watch/info/%s'>%s</a>" %(curpage-1,'上一页'))
        next_html = mark_safe("<a href='/watch/info/%s'>%s</a>" %(curpage+1,'下一页'))
        
    for i in list(range(1,max_page+1)):
        #首页上一页
        if i == 1:
            p = mark_safe("<a href='/watch/info/%s'>%s</a>" %(1,'首页'))
            page_html_l.append(p)
            page_html_l.append(pre_html)
        
        #1.可以显示的页码
        if curpage-marginnum < i and i < curpage:
            p = mark_safe("<a href='/watch/info/%s'>%s</a>" %(i,i))
            page_html_l.append(p)
#         #左边省略号...
#         elif i==curpage-3:
#             p = mark_safe("<a>...</a>") 
#             page_html_l.append(p)
        #中间的页码
        elif i==curpage:
            p = mark_safe("<a style='color:red' href='/watch/info/%s'>%s</a>" %(i,i))
            page_html_l.append(p)
        #右边显示的页码
        elif i>=curpage and i<curpage+marginnum:
            p = mark_safe("<a href='/watch/info/%s'>%s</a>" %(i,i))
            page_html_l.append(p)
            
#         #右边省略号...
#         elif i == curpage+3:           
#             p = mark_safe("<a>...</a>")
#             page_html_l.append(p) 
#         
        
        #末页下一页
        if i == max_page:
            p = mark_safe("<a href='/watch/info/%s'>%s</a>" %(max_page,'末页'))
            page_html_l.append(next_html)
            page_html_l.append(p)

    return page_html_l