# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib

from log import log

def get_baidu_cookie():
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.open('https://www.baidu.com')
    for item in cookie:
        print 'Name = ' + item.name
        print 'Value = ' + item.value


def save_cookie_to_file():
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.open('https://www.baidu.com')
    cookie.save(ignore_discard=True, ignore_expires=True)


def get_cookie_from_file():
    cookie = cookielib.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    req = urllib2.Request('http://www.baidu.com')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print response.read()


def login_simulation():
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
        'email': 'jsculsp@126.com',
        'password': '***',
        '_xsrf': 'a2a06a71dfe6c89bc6b7399819e52639',
        'captcha_type': 'cn',
    })
    headers = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': '*/*',
        'Origin': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.zhihu.com/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    loginUrl = 'https://www.zhihu.com/login/email'
    req1 = urllib2.Request(loginUrl, data=postdata, headers=headers)
    try:
        opener.open(req1)
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return
    cookie.save(ignore_discard=True, ignore_expires=False)
    homeUrl = 'https://www.zhihu.com/'
    req2 = urllib2.Request(homeUrl, headers=headers)
    result = opener.open(req2)
    print result.read().decode('utf-8', 'ignore').encode('gbk', 'ignore')