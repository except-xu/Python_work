# !/bin/env python3
# -*- coding: utf-8 -*


# ================================= 以下代码不懂不要随便乱动 ====================================
try:
    import requests
    import json
    import sys
    import os
    import re
    import time
    from loguru import logger
except Exception as e:
    logger.error(e)
requests.packages.urllib3.disable_warnings()
# --------------------------------------------------------------------------------------------
Script_Name = "特步"
Name_Pinyin = "tebu"
Script_Change = "特步商城签到 ,第一个 py 脚本"
Script_Version = "0.0.1"
Version_Check = "0.0.1"


# --------------------------------------------------------------------------------------------

def last_version(name, mold):
    url = ''
    if mold == 1:
        url = "https://raw.gh.fakev.cn/yml2213/Python/master/" + name + "/" + name + ".py"
    elif mold == 2:
        url = "http://yml-gitea.ml:2233/yml/JavaScript-yml/raw/branch/master/" + name + ".py"
    try:
        _url = url
        _headers = {}
        response = requests.get(url=_url, headers=_headers, verify=False)
        result = response.text
        r = re.compile(r'Version_Check = "(.*?)"')
        data1 = r.findall(result)
        return data1[0]
    except Exception as err:
        print(err)


def mac_env(tebu_data):
    global ckArr
    pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
    path = pwd + ".env"
    with open(path, "r+") as f:
        env = f.read()
        if tebu_data in env:
            r = re.compile(r'tebu_data="(.*?)"', re.M | re.S | re.I)
            result = r.findall(env)
            # print(data[0])
            if "@" in result[0]:
                _ck = result[0].split("@")
                ckArr = _ck
            elif "\n" in result[0]:
                _ck = result[0].split("\n")
                ckArr = _ck
            else:
                ckArr = result
        else:
            logger.warning("检查变量" + tebu_data + "是否已填写")


def ql_env(tebu_data):
    global ckArr
    if tebu_data in os.environ:
        ckArr = []
        _data = os.environ[tebu_data]
        if "@" in _data:
            _ck = _data.split("@")
            ckArr = _ck
        elif "\n" in _data:
            _ck = _data.split("\n")
            ckArr = _ck
        else:
            ckArr = _data


mac_env("tebu_data")
ql_env("tebu_data")


class Tpyqc:
    def __init__(self, phone, passwd):
        self.phone = phone
        self.passwd = passwd

    url_login = "https://mrobot.pcauto.com.cn/auto_passport3_back_intf/passport3/rest/login_new.jsp"

    def login(self):
        data_login = "password=" + self.passwd + "&username=" + self.phone
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            response = requests.post(url=self.url_login, headers=headers, data=data_login, verify=False)
            result = response.json()

            if result["status"] == 0:
                # if result.status == 0:
                logger.info("登录: " + result["message"] + ' ,更新 session 成功')
                logger.info("")
                session = result["session"]

            else:
                logger.error("登录失败 ,请检查 变量 是否正确!")
        except Exception as err:
            print(err)
            # msg("【账号{}】签到失败 ,可能是Cookie过期".format(account))


# 获取通知服务
class msg(object):
    def __init__(self, m=""):
        self.str_msg = m
        self.message()

    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()  # 这代码的作用就是刷新缓冲区。
        # 当我们打印一些字符时 ,并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区 ,然后再打印。
        # 这就存在一个问题 ,如果你想等时间间隔的打印一些字符 ,但由于缓冲区没满 ,不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。

    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = "https://gitee.com/curtinlv/Public/raw/master/sendNotify.py"
            response = requests.get(url)
            if "curtinlv" in response.text:
                with open("sendNotify.py", "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass

    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")


msg().main()


def tip():
    global ckArr
    logger.info("================ 脚本只支持青龙新版 =================")
    logger.info("============ 具体教程以请自行查看顶部教程 =============\n")
    logger.info("🔔 " + Script_Name + " ,开始!")
    # origin_version = last_version(Name_Pinyin, 1)
    # logger.info("📌 本地脚本: V " + Script_Version +
    #             "    远程仓库版本: V" + origin_version)
    logger.info("📌 🆙 更新内容: " + Script_Change)
    print(len(ckArr))
    # logger.info("共发现 " + len(ckArr) + "个账号!")


if __name__ == "__main__":
    global msg_info
    global ckArr
    tip()
    for data in ckArr:
        ck = data.split("&")
        Tpyqc = Tpyqc(ck[0], ck[1])
        logger.info("开始 登录")
        # Tpyqc.login()
