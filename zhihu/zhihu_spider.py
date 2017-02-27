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
    try:
        cookie = cookielib.MozillaCookieJar()
        cookie.load(filename, ignore_discard=True, ignore_expires=True)
    except:
        cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    return cookie, opener


def login(password):
    cookie, opener = generate_opener()
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
    return True


def visit_by_url(password, url, filename):
    flag = login(password)
    if flag == False:
        print('login failed, please check your log file...')
    _, opener = generate_opener()
    req = urllib2.Request(url, headers=headers)
    result = opener.open(req)
    path = os.path.join(PROJECT_ROOT, 'zhihu/pages', filename)
    with open(path, 'w') as f:
        f.write(result.read())
    print('success!')