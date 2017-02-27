# -*- coding:utf-8 -*-
import os
import sys
import urllib
import urllib2
import cookielib

from ..log import log

PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(1, PROJECT_ROOT)

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


def generate_opener():
    filename = os.path.join(PROJECT_ROOT, 'zhihu/cookie.txt')
    cookie = cookielib.MozillaCookieJar()
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    return cookie, opener


def login(password):
    filename = os.path.join(PROJECT_ROOT, 'zhihu/cookie.txt')
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
        'email': 'jsculsp@126.com',
        'password': password,
        '_xsrf': 'f2d467cceb2be896f51a69b6db691810',
        'captcha_type': 'cn',
    })
    loginUrl = 'https://www.zhihu.com/login/email'
    req = urllib2.Request(loginUrl, data=postdata, headers=headers)
    try:
        opener.open(req)
    except urllib2.HTTPError, e:
        log(e.code, e.reason)
        return False
    cookie.save(ignore_discard=True, ignore_expires=False)
    return cookie, opener


def visit_by_url():
    url = raw_input(u'请输入你想访问的 URL: \r\n'.encode('gbk'))
    filename = raw_input(u'请输入保存的文件的文件名(后缀为 .html)：\r\n'.encode('gbk'))
    req = urllib2.Request(url, headers=headers)
    try:
        _, opener = generate_opener()
    except cookielib.LoadError:
        password = raw_input(u'cookie 文件不存在，请重新输入你的密码：\r\n'.encode('gbk'))
        _, opener = login(password)
    try:
        result = opener.open(req)
    except urllib2.HTTPError:
        password = raw_input(u'你的 cookie 已经过期，请重新输入你的密码：\r\n'.encode('gbk'))
        _, opener = login(password)
        result = opener.open(req)
    if result == False:
        print(u'login failed, please check your log file...')
        return
    path = os.path.join(PROJECT_ROOT, 'zhihu/pages', filename)
    with open(path, 'w') as f:
        f.write(result.read())
    print(u'success!')