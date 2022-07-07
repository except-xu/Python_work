#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DiDi_exchange.py
Author: 一风一燕
功能: 滴滴出行积分派兑
Date: 2021-11-20
cron: 29,59 8,9,14,18 * * * xF_DiDi_exchange.py
new Env('滴滴出行积分派兑');


Updata:2021-12-03
1、更新goods_id无需自己抓取 ,只需要运行一次脚本 ,日志自行输出优惠券goods_id。教程继续保留抓包 ,万一有一天无法输出 ,可根据教程抓包。
2、滴滴抢券时间有9点 ,15点 ,8点30分 ,和18点30分 ,所以需要自行调整cron ,29 8,18 * * * 或者 59 8,14 * * * ,脚本会自适应调整抢购时间。


****************滴滴出行APP*******************


【教程】: 需要自行用手机抓取Didi_jifen_token。
在青龙变量中添加变量Didi_jifen_token
多个账号时 ,Didi_jifen_token ,用&隔开 ,例如Didi_jifen_token=xxxxx&xxxx
Didi_jifen_token如何抓 ,请看didi_Sign说明


手机抓包后 ,点击一下要兑换的优惠券 ,查看URL ,https://magma.xiaojukeji.com/sessionActivity/info?
在JSON中就搜索你要抢券的名字 ,例如9折快车券 ,发现good_name: "9折快车券" ,再往下一点 ,就会有个id="176234",其中这个数字就是你要兑换的优惠券id ,填写至青龙变量即可


在青龙变量中添加变量goods_id='176234' ,其中这个数字就是你刚刚抓包要兑换的优惠券id。

如果是多账号 ,在青龙变量中添加变量DiDi_accout="1" ,就是账号1抢优惠券 ,填2 ,就是账号2抢券。目前只支持单个号抢 ,后续考虑增加并发抢券功能。默认抢【账号1】

cron时间填写: 29,59 8,9,14,18 * * *



'''

Didi_jifen_token = ''
DiDi_accout = '1'

'''




=================================以下代码不懂不要随便乱动=================================


'''

try:
    import requests
    import json, sys, os, re
    import time, datetime
except Exception as e:
    print (e)

tokens = ''
goods_id = ''

starttime = '00:00:00.00000000'
endtime = '00:00:30.00000000'
nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
today = datetime.datetime.now ().strftime ('%Y-%m-%d')
mor_time = '08:00:00.00000000'
mor_time2 = '08:40:00.00000000'
mid_time = '11:00:00.00000000'
aft_time = '15:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)
moringtime2 = '{} {}'.format (today, mor_time2)
middle_time = '{} {}'.format (today, mid_time)
afternoon_time = '{} {}'.format (today, aft_time)
if nowtime > moringtime and nowtime < moringtime2:
    # 开始抢兑时间
    starttime = '08:29:59.00000000'
    # 结束时间
    endtime = '08:30:30.00000000'
elif nowtime > moringtime2 and nowtime < middle_time:
    # 开始抢兑时间
    starttime = '08:59:59.00000000'
    # 结束时间
    endtime = '09:00:30.00000000'
elif nowtime > middle_time and nowtime < afternoon_time:
    # 开始抢兑时间
    starttime = '14:59:59.00000000'
    # 结束时间
    endtime = '15:00:30.00000000'
elif nowtime > afternoon_time:
    # 开始抢兑时间
    starttime = '18:29:59.00000000'
    # 结束时间
    endtime = '18:30:30.00000000'

requests.packages.urllib3.disable_warnings ()

pwd = os.path.dirname (os.path.abspath (__file__)) + os.sep
path = pwd + "env.sh"

today = datetime.datetime.now ().strftime ('%Y-%m-%d')
tomorrow = (datetime.datetime.now () + datetime.timedelta (days=1)).strftime ('%Y-%m-%d')
qgtime = '{} {}'.format (today, starttime)
qgendtime = '{} {}'.format (today, endtime)


def printT(s):
    print ("[【{0}】]: {1}".format (datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush ()


def getEnvs(label):
    try:
        if label == 'True' or label == 'yes' or label == 'true' or label == 'Yes':
            return True
        elif label == 'False' or label == 'no' or label == 'false' or label == 'No':
            return False
    except:
        pass
    try:
        if '.' in label:
            return float (label)
        elif '&' in label:
            return label.split ('&')
        elif '@' in label:
            return label.split ('@')
        else:
            return int (label)
    except:
        return label


##############      在pycharm测试ql环境用 ,实际用下面的代码运行      #########

# with open(path, "r+", encoding="utf-8") as f:
#    ck = f.read()
#    tokens = ck
#    if "Didi_jifen_token" in ck:
#        r = re.compile (r'Didi_jifen_token="(.*?)"', re.M | re.S | re.I)
#        tokens = r.findall(ck)
#        tokens = tokens[0].split ('&')
#        DiDi_accout = int (DiDi_accout) - 1
#        tokens = tokens[DiDi_accout]
#        print(tokens)
#        if len (tokens) == 1:
#            Didi_jifen_token = tokens[0]
#            tokens = ''
#            # print(tokens)
#            # tokens = token[3]
#        else:
#            pass
#    printT ("已获取并使用ck环境 token")


########################################################################

if "Didi_jifen_token" in os.environ:
    print (len (os.environ["Didi_jifen_token"]))
    if len (os.environ["Didi_jifen_token"]) > 419:
        tokens = os.environ["Didi_jifen_token"]
        # tokens = tokens.split ('&')
        # token = temporary[0]
        printT ("已获取并使用Env环境Didi_jifen_token")
    else:
        Didi_jifen_token = os.environ["Didi_jifen_token"]
else:
    print ("检查变量Didi_jifen_token是否已填写")

if "goods_id" in os.environ:
    goods_id = os.environ["goods_id"]
    printT (f"已获取并使用Env环境goods_id={goods_id}")
else:
    print ("goods_id未填写 ,不兑换")
    # exit(0)

if "DiDi_accout" in os.environ:
    DiDi_accout = os.environ["DiDi_accout"]
    printT (f"已获取并使用Env环境DiDi_accout ,【账号{DiDi_accout}】抢券")
    if tokens != '':
        DiDi_accout = int (DiDi_accout) - 1
    # tokens = tokens[DiDi_accout]


else:
    print ("DiDi_accout未填写 ,默认【账号1】抢券")


## 获取通知服务
class msg (object):
    def __init__(self, m=''):
        self.str_msg = m
        self.message ()

    def message(self):
        global msg_info
        printT (self.str_msg)
        try:
            msg_info = "{}\n{}".format (msg_info, self.str_msg)
        except:
            msg_info = "{}".format (self.str_msg)
        sys.stdout.flush ()  # 这代码的作用就是刷新缓冲区。
        # 当我们打印一些字符时 ,并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区 ,然后再打印。
        # 这就存在一个问题 ,如果你想等时间间隔的打印一些字符 ,但由于缓冲区没满 ,不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。

    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get (url)
            if 'curtinlv' in response.text:
                with open ('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write (response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify (a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify (a)
            else:
                pass

    def main(self):
        global send
        cur_path = os.path.abspath (os.path.dirname (__file__))
        sys.path.append (cur_path)
        if os.path.exists (cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify ()
                try:
                    from sendNotify import send
                except:
                    printT ("加载通知服务失败~")
        else:
            self.getsendNotify ()
            try:
                from sendNotify import send
            except:
                printT ("加载通知服务失败~")
        ###################


msg ().main ()
nowtime = int (round (time.time () * 1000))

uid = ''

if tokens != '':
    # if "Didi_jifen_token" in tokens:
    # r = re.compile (r'Didi_jifen_token="(.*?)"', re.M | re.S | re.I)
    # tokens = r.findall (ck)
    tokens = tokens.split ('&')
    # print(tokens)
    if len (tokens) == 1:
        Didi_jifen_token = tokens[0]

    else:
        pass


# 获取优惠券good_id
def get_goodid(Didi_jifen_token):
    try:
        url = f'https://magma.xiaojukeji.com/sessionActivity/info?source_id=z10000&partition_id=1002&pid=10004&token={Didi_jifen_token}&city_id=21&cityId=21&lat=23.016388346354166&lng=113.81221218532986&wsgsig=dd03-aScF%2FD3Xy4FqxzWqMzcXogciSvVXYQRtNv7%2FYmClSvVWxo8R58nVS0KUxKFWx8frH43PpggVz3HVRJ3x2z8wYgNlxR6yPzfqM%2BNhZg7%2FzKHjx3Nr2z7kTXDVwKE'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://page.udache.com/",
            "Host": "magma.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            # "content-type":"application/x-www-form-urlencoded;charset=utf-8",
        }
        response = requests.get (url=url, headers=headers, verify=False)
        result = response.json ()
        # print(result)
        id = result['data']['list']

        for i in range (len (id)):
            try:
                goods_id = id[i]['goods_ids']
                k = len (goods_id)
                name1 = id[i]['goods_list'][0]['info']['goods_info']['goods_name']
                goods_id1 = id[i]['goods_ids'][0]
                if k == 2:
                    name2 = id[i]['goods_list'][1]['info']['goods_info']['goods_name']
                    goods_id2 = id[i]['goods_ids'][1]
                if i == 0:
                    print ("今天【第一场次】优惠券{0} ,good_id为【{1}】".format (name1, goods_id1))
                    if k == 2:
                        print (("今天【第一场次】优惠券{0} ,good_id为【{1}】".format (name2, goods_id2)))
                elif i == 1:
                    print ("今天【第二场次】优惠券{0} ,good_id为【{1}】".format (name1, goods_id1))
                    if k == 2:
                        print ("今天【第二场次】优惠券{0} ,good_id为【{1}】".format (name2, goods_id2))
                elif i == 2:
                    print ("明天【第一场次】优惠券{0} ,good_id为【{1}】".format (name1, goods_id1))
                    if k == 2:
                        print ("明天【第一场次】优惠券{0} ,good_id为【{1}】".format (name2, goods_id2))
                else:
                    print ("明天【第二场次】优惠券{0} ,good_id为【{1}】".format (name1, goods_id1))
                    if k == 2:
                        print ("明天【第二场次】优惠券{0} ,good_id为【{1}】".format (name2, goods_id2))
                        break
                    break
            except Exception as e:
                print (e)


    except Exception as e:
        print (e)
        msg ("【账号{0}】获取优惠券id失败,可能是token过期".format (DiDi_accout))


# 兑换
def do_Lottery(Didi_jifen_token, goods_id, DiDi_accout):
    print ("抢券帐号token为{}".format (Didi_jifen_token))
    try:
        url = f'https://magma.xiaojukeji.com/order/create?wsgsig=dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Accept-Encoding": "gzip, deflate, br",
            # "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://page.udache.com/",
            "Host": "magma.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "content-length": "2444",
        }
        data = f'source_id=z10000&partition_id=1002&pid=10004&token={Didi_jifen_token}&city_id=21&cityId=21&lat=23.01633110894097&lng=113.81249403211805&goods_id={goods_id}&pay_number=1&env=%7B%22latitude%22:%2223.01633110894097%22,%22longitude%22:%22113.81249403211805%22,%22city_id%22:%2221%22,%22ddfp%22:%2299d8f16bacaef4eef6c151bcdfa095f0%22,%22fromPage%22:%22https:%2F%2Fpage.udache.com%2Fut-mall%2Fxmall%2Findex.html%3Fchannel_id%3D72%252C278%252C80505%26entrance_channel%3D7227880505%26xsc%3D%26dchn%3D6xzREaa%26prod_key%3Dcustom%26xbiz%3D%26xpsid%3D5ea8b7c9f92f4ed3bbd374f11673a5f5%26xenv%3Dpassenger%26xspm_from%3D%26xpsid_from%3D%26xpsid_root%3D5ea8b7c9f92f4ed3bbd374f11673a5f5%26appid%3D10000%26lang%3Dzh-CN%26clientType%3D1%26trip_cityid%3D21%26datatype%3D101%26imei%3D99d8f16bacaef4eef6c151bcdfa095f0%26channel%3D102%26appversion%3D6.2.4%26trip_country%3DCN%26TripCountry%3DCN%26lng%3D113.812494%26maptype%3Dsoso%26os%3DiOS%26utc_offset%3D480%26location_cityid%3D21%26access_key_id%3D1%26deviceid%3D99d8f16bacaef4eef6c151bcdfa095f0%26cityid%3D21%26location_country%3DCN%26phone%3DUCvMSok42%2B5%2BtfafkxMn%2BA%253D%253D%26model%3DiPhone11%26lat%3D23.016331%26origin_id%3D1%26client_type%3D1%26terminal_id%3D1%26sig%3D1b0201bd0b2a72e15601472602f5c0048bb4062a%23%2Forder-virtual%3Fid%3D176234%26channel_id%3D72,278,80505%26entrance_channel%3D7227880505%26xsc%3D%26dchn%3D6xzREaa%26prod_key%3Dcustom%26xbiz%3D%26xpsid%3D5ea8b7c9f92f4ed3bbd374f11673a5f5%26xenv%3Dpassenger%26xspm_from%3D%26xpsid_from%3D%26xpsid_root%3D5ea8b7c9f92f4ed3bbd374f11673a5f5%26appid%3D10000%26lang%3Dzh-CN%26clientType%3D1%26trip_cityid%3D21%26datatype%3D101%26imei%3D99d8f16bacaef4eef6c151bcdfa095f0%26channel%3D102%26appversion%3D6.2.4%26trip_country%3DCN%26TripCountry%3DCN%26lng%3D113.812494%26maptype%3Dsoso%26os%3DiOS%26utc_offset%3D480%26location_cityid%3D21%26access_key_id%3D1%26deviceid%3D99d8f16bacaef4eef6c151bcdfa095f0%26cityid%3D21%26location_country%3DCN%26phone%3DUCvMSok42%252B5%252BtfafkxMn%252BA%253D%253D%26model%3DiPhone11%26lat%3D23.016331%26origin_id%3D1%26client_type%3D1%26terminal_id%3D1%26sig%3D1b0201bd0b2a72e15601472602f5c0048bb4062a%22,%22partition_id%22:%221002%22,%22openId%22:%22%22,%22isOpenWeb%22:true,%22isHitButton%22:true,%22appid%22:10000%7D'
        printT (f"抢购时间为: {qgtime}")
        printT (f"正在等待兑换时间 ,请勿终止退出...")
        while True:
            nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
            if nowtime > qgtime:
                response = requests.post (url=url, headers=headers, verify=False, data=data)
                result = response.json ()
                print (result)
                errmsg = result['errmsg']
                if "商品已下线" in errmsg:
                    msg ("商品已下线,无法兑换".format (DiDi_accout))
                    break
                else:
                    is_started = result['data']['is_started']
                    is_repeat = result['data']['is_repeat']
                    is_soldout = result['data']['is_soldout']
                if errmsg == 'ok' and is_started == 1 and is_repeat == 1:
                    msg ("【账号{0}】【{1}】优惠券兑换成功".format (DiDi_accout,goods_id))
                    break

                elif nowtime > qgendtime:
                    if is_soldout == 1:
                        msg ("【账号{0}】兑换失败 ,优惠券被抢空了 ,又或者是未到抢券场次".format (DiDi_accout))
                    else:
                        msg ("【账号{0}】兑换失败 ,检查是否已到抢券场次".format (DiDi_accout))
                    break

    except Exception as e:
        print (e)
        msg ("【账号{0}】兑换失败,可能是token过期".format (DiDi_accout))


if __name__ == '__main__':
    print ("============脚本只支持青龙新版=============\n")
    print ("具体教程以文本模式打开文件 ,查看顶部教程\n\n")
    print ("============执行滴滴积分派兑脚本==============")
    print (Didi_jifen_token)
    if Didi_jifen_token != '':
        msg ("单账号模式")
        get_goodid (Didi_jifen_token)
        if goods_id != '':
            do_Lottery (Didi_jifen_token, goods_id, DiDi_accout)
        else:
            msg ("goods_id未填写 ,不兑换")
    elif tokens == '':
        print ("检查变量Didi_jifen_token是否已填写")
    else:
        msg (f"单账号兑换模式 ,【账号{DiDi_accout + 1}】进行兑换")
        get_goodid (tokens[int (DiDi_accout)])
        if goods_id != '':
            tokens = tokens[int (DiDi_accout)]

            do_Lottery (tokens, goods_id, DiDi_accout + 1)
        else:
            msg ("goods_id未填写 ,不兑换")
    # msg("多账号模式")
    # for i in tokens:             #同时遍历两个list ,需要用ZIP打包
    #     get_activity_info (i, day,numb,DiDi_accout)
    #     reward (i, day,numb,DiDi_accout)
    #     activity_id = get_lid()
    #     if do_lottery == 'true':
    #         do_Lottery (i,activity_id,DiDi_accout)
    #     DiDi_accout += 1

    if "兑换成功" in msg_info:
        send ("滴滴积分兑换", msg_info)
    elif "秒杀商品" in msg_info:
        send ("滴滴积分兑换", msg_info)
    elif "过期" in msg_info:
        send ("滴滴积分兑换", msg_info)
