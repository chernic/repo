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
    try:
        html = openurl(req).read().decode('gbk')
    except Exception as e:
        return False
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
    try:
        html = openurl(pre_login).read().decode('gbk')
    except Exception as e:
        return False
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
        'note'           :   "+++ ^_^",
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

    try:
        html = openurl('http://www.178448.com/home.php?mod=spacecp&ac=friend&op=find').read(100000).decode('gbk')
    except Exception as e:
        print('INFO : openurl失败!')
        exit(0)

    patt = re.compile(r'坛友互动 \((.*?)\)\'')
    hd = patt.search(html)
    hd = hd.group(1)
    print('INFO : 当前坛友互动数量为: %s' % hd)
    patt = re.compile(r'积分: (.*?)<')
    jf = patt.search(html)
    jf = jf.group(1)
    print('INFO : 当前用户积分数量为: %s' % jf)

    file_object = open('try_to_offlineadd.txt')
    try:
        #2017-10-18 : 411800
        Numb = file_object.read( )
        if Numb == "":
            Numb=411800
    finally:
         file_object.close( )

    file_write = open( jf+ '_' +hd+ '.log', 'w+')
    
    for times in range(0, -30000, -1):
        XNumb = int(Numb) + int(times)
        file_write.write("addfriend_dz(uid=%s, domain=dom)\n" % str(XNumb) )
        flag = addfriend_dz(uid=str(XNumb), domain=dom)
        if flag :
            print("[OK] addfriend_dz(uid=%s, domain=dom)" % str(XNumb) )
        else :
            print("[NK] addfriend_dz(uid=%s, domain=dom)" % str(XNumb) )
        file_object = open('try_to_offlineadd.txt', 'w')
        file_object.write(str(XNumb))
        file_object.close( )
    file_write.close( )

except Exception as e:
    print('Error:',e)
