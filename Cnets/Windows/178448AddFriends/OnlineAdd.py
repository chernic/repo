#!/usr/bin/python
# -*- coding: GBK -*-
import  urllib.request
import  urllib.parse
import  http.cookiejar,re
import  datetime,time

opener = None
# 带Cookie访问
def openurl(parms):
  global opener
  if opener == None:
      #cookie设置
      cj =  http.cookiejar.CookieJar()
      opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  ret = opener.open(parms)
  return ret

'''
 通用的登陆论坛
 参数说明parms:
   username:用户名(必填),
   password :密码(必填),
   domain:网站域名，注意格式必须是：http://www.xxx.xx/(必填),
   answer:问题答案,
   questionid:问题ID,
   referer:跳转地址

   这里使用了可变关键字参数(相关信息可参考手册)
'''
def login_dz(**parms):
  # Form item: "formhash" = "0fec3b17"
  # Form item: "loginfield" = "username"

  # Form item: "answer" = ""
  # Form item: "password" = "5aeb467c2154c4ac3565795c8582996c"
  # Form item: "questionid" = "0"
  # Form item: "referer" = "http://www.178448.com/space-uid-313672.html"
  # Form item: "username" = "chernic"
  #初始化
  parms_key = ['domain','answer','password','questionid','referer','username']
  arg = {}
  for key in parms_key:
    if key in parms:
      arg[key] = parms[key]
    else:
      arg[key] = ''

  #获取 formhash
  pre_login = arg['domain']+'member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
  html = openurl(pre_login).read().decode('gbk')
  patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
  formhash = patt.search(html)
  if not formhash:
    raise Exception('GET formhash Fail!')
  formhash = formhash.group(1)

  #登陆
  postdata = {
   'answer':arg['answer'],
   'formhash':formhash,
   'password':arg['password'],
   'questionid':0 if arg['questionid']=='' else arg['questionid'],
   'referer':arg['domain'] if arg['referer']=='' else arg['referer'],
   'username':arg['username'],
    }
  postdata = urllib.parse.urlencode(postdata)
  postdata = postdata.encode('utf-8')
  req = urllib.request.Request(
# http://www.178448.com/member.php?mod=logging&action=login&loginsubmit=yes&frommessage&loginhash=LT6yC&inajax=1
    # url= arg['domain']+'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LCaB3&inajax=1',
    url= arg['domain']+'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LT6yC&inajax=1',
    data=postdata
    )
  html = openurl(req).read().decode('gbk')
  # 假设返回假
  flag = False
  if 'succeedhandle_login' in html:
    flag = True
  return flag

def addfriend_dz(**parms):
    #初始化
    parms_key = ['domain', 'answer', 'password', 'questionid', 'referer', 'username', 'uid']
    arg = {}
    for key in parms_key:
        if key in parms:
            arg[key] = parms[key]
        else:
            arg[key] = ''

    #获取 formhash
    pre_login = arg['domain']+'home.php?mod=spacecp&ac=friend&op=add&uid='+ arg['uid'] +'&inajax=1'
    html = openurl(pre_login).read().decode('gbk')
    patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
    formhash = patt.search(html)

    # 判断返回
    if not formhash:
        # <div class="alert_info">正在等待验证
        # raise Exception('GET formhash Fail!')
        # 退出不报错
        # print('INFO : 获取失败 formhash !')
        return False
    #<em id="return_">加为好友</em>
    formhash = formhash.group(1)

    postdata = {
        'referer'        :   "http://www.178448.com/home.php?mod=spacecp&ac=friend&op=find",
        'addsubmit'      :   "true",
        'handlekey'      :   "a_online_friend_" + arg['uid'],
        'formhash'       :   formhash,
        'note'           :   "+++ ^_^ OK ???",
        'gid'            :   "1",
    }
    postdata = urllib.parse.urlencode(postdata)
    postdata = postdata.encode('utf-8')
    req = urllib.request.Request(
        url= arg['domain']+'home.php?mod=spacecp&ac=friend&op=add&uid='+ arg['uid'] +'&inajax=1',
        data=postdata
        )
    html = openurl(req).read().decode('gbk')

    # 判断返回
    if 'succeedhandle_a_online_friend' in html:
        # print("INFO : OK ", arg['uid'])
        return True
    else :
        # print("INFO : NK ", arg['uid'])
        return False

# 测试网站
# http.request.method==POST
dom='http://www.178448.com/'
try:
    flag = login_dz(username="chernic",password="a147258369",domain=dom)
    if not flag:
        print('INFO : 登陆失败!')
        exit(0)
    else:
        print('INFO : 登陆成功')

    html = openurl('http://www.178448.com/home.php?mod=spacecp&ac=friend&op=find').read(100000).decode('gbk')
    patt = re.compile(r'坛友互动 \((.*?)\)\'')
    hd = patt.search(html)
    hd = hd.group(1)
    print('INFO : 当前坛友互动数量为: %s' % hd)
    patt = re.compile(r'积分: (.*?)<')
    jf = patt.search(html)
    jf = jf.group(1)
    print('INFO : 当前用户积分数量为: %s' % jf)

    file_object = open( jf+ '_' +hd+ '.log', 'w+')
    AllTimes=0
    imes=0
    for times in range(1, 50):
        html = openurl('http://www.178448.com/home.php?mod=spacecp&ac=friend&op=find').read(100000).decode('gbk')
        patt = re.compile(r'a_online_friend_(.*?)"')
        numbs = patt.findall(html)
        x=0
        for numb in numbs :
            x=x+1
            flag = addfriend_dz(uid=numb, domain=dom)
            if flag :
                print("[%s %d/%d]addfriend_dz(uid=%s) hd=[%s]" % (times, x, len(numbs), numb, hd) )
                file_object.write("[%s %d/%d]addfriend_dz(uid=%s)\n" % (times, x, len(numbs), numb) )
                AllTimes = AllTimes +1
    file_object.close( )

    file_object = open('try_to_add.txt', 'a')
    file_object.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S") + ' = ' + str(AllTimes) )
    file_object.close( )

except Exception as e:
    print('Error:',e)

# 参考链接 http://t.cn/RO3sHVT
'''  登录抓包结果
Frame 131: 1130 bytes on wire (9040 bits), 1130 bytes captured (9040 bits) on interface 0
Ethernet II, Src: LanAcces_cc:ac:a4 (00:20:be:cc:ac:a4), Dst: Tp-LinkT_fe:a8:ba (30:fc:68:fe:a8:ba)
Internet Protocol Version 4, Src: 192.168.2.137, Dst: 121.40.22.8
Transmission Control Protocol, Src Port: 6771, Dst Port: 80, Seq: 1, Ack: 1, Len: 1076
Hypertext Transfer Protocol
    POST /member.php?mod=logging&action=login&loginsubmit=yes&frommessage&loginhash=LT6yC&inajax=1 HTTP/1.1\r\n
    Host: www.178448.com\r\n
    User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0 Light/49.0\r\n
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
    Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n
    Accept-Encoding: gzip, deflate\r\n
    Referer: http://www.178448.com/space-uid-313672.html\r\n
     [truncated]Cookie: UM_distinctid=15f0bdf3cfe10e-09ac392205e2718-1b110873-100200-15f0bdf3d00138; CNZZDATA1613261=cnzz_eid%3D1932572803-1507727884-%26ntime%3D1508230768; ad_play_index=57; c448_2ce1_sid=WnYybp; c448_2ce1_noticeTitle=1; c448_
    DNT: 1\r\n
    Connection: keep-alive\r\n
    Upgrade-Insecure-Requests: 1\r\n
    Content-Type: application/x-www-form-urlencoded\r\n
    Content-Length: 177\r\n
    \r\n
    [Full request URI: http://www.178448.com/member.php?mod=logging&action=login&loginsubmit=yes&frommessage&loginhash=LT6yC&inajax=1]
    [HTTP request 1/1]
    File Data: 177 bytes
HTML Form URL Encoded: application/x-www-form-urlencoded
    Form item: "formhash" = "0fec3b17"
    Form item: "referer" = "http://www.178448.com/space-uid-313672.html"
    Form item: "loginfield" = "username"
    Form item: "username" = "chernic"
    Form item: "password" = "5aeb467c2154c4ac3565795c8582996c"
    Form item: "questionid" = "0"
    Form item: "answer" = ""
'''
'''  添加抓包结果
Frame 1270: 145 bytes on wire (1160 bits), 145 bytes captured (1160 bits) on interface 0
Ethernet II, Src: LanAcces_cc:ac:a4 (00:20:be:cc:ac:a4), Dst: Tp-LinkT_fe:a8:ba (30:fc:68:fe:a8:ba)
Internet Protocol Version 4, Src: 192.168.2.137, Dst: 121.40.22.8
Transmission Control Protocol, Src Port: 7304, Dst Port: 80, Seq: 6598, Ack: 11744, Len: 91
[2 Reassembled TCP Segments (1551 bytes): #1269(1460), #1270(91)]
Hypertext Transfer Protocol
    POST /home.php?mod=spacecp&ac=friend&op=add&uid=337916&inajax=1 HTTP/1.1\r\n
    Host: www.178448.com\r\n
    User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0 Light/49.0\r\n
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
    Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n
    Accept-Encoding: gzip, deflate\r\n
    Referer: http://www.178448.com/home.php?mod=spacecp&ac=friend&op=find\r\n
     [truncated]Cookie: UM_distinctid=15f0bdf3cfe10e-09ac392205e2718-1b110873-100200-15f0bdf3d00138; CNZZDATA1613261=cnzz_eid%3D1932572803-1507727884-%26ntime%3D1508230768; ad_play_index=58; c448_2ce1_sid=jMaRBX; c448_2ce1_saltkey=SGTQJ2Lx; c4
    DNT: 1\r\n
    Connection: keep-alive\r\n
    Upgrade-Insecure-Requests: 1\r\n
    Content-Type: application/x-www-form-urlencoded\r\n
    Content-Length: 172\r\n
    \r\n
    [Full request URI: http://www.178448.com/home.php?mod=spacecp&ac=friend&op=add&uid=337916&inajax=1]
    [HTTP request 5/11]
    [Prev request in frame: 1232]
    [Next request in frame: 1271]
    File Data: 172 bytes
HTML Form URL Encoded: application/x-www-form-urlencoded
    Form item: "referer" = "http://www.178448.com/home.php?mod=spacecp&ac=friend&op=find"
    Form item: "addsubmit" = "true"
    Form item: "handlekey" = "a_online_friend_337916"
    Form item: "formhash" = "660027b1"
    Form item: "note" = "112233"
    Form item: "gid" = "1"

    http://www.178448.com/home.php?mod=spacecp&ac=friend&op=add&uid=337916&handlekey=onlinehk_337916
    337916
'''
