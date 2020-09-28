import requests

res = None


class HttpRequest:
    """用于发起HTTP请求"""

    def http_request(self, method, url, param, cookies):
        global res

        if method.upper() == "GET":
            try:
                res = requests.get(url, params=param, cookies=cookies)  # request/requests
            except Exception as e:
                print("get请求出错了:{}".format(e))
        elif method.upper() == "POST":
            try:
                res = requests.post(url, data=param, cookies =cookies)    # post 是data而不是param
            except Exception as e:
                print("post请求出错了:{}".format(e))
        else:
            print("不支持该请求方式")
            res = None
        return res


if __name__ == '__main__':
    url = "http://test.lemonban.com/futureloan/mvc/api/member/register"
    param = {'mobilephone': '18300070752', 'pwd': '12345678', 'regname': '李大莉'}
    method = "get"
    resp = HttpRequest().http_request(method, url, param)
    print(resp.text)
# 1、报错AttributeError: 'NoneType' object has no attribute 'text'
# 不支持该请求方式
# 原因输入的变量与类的变量顺序不一致
# 2、报错服务器异常，服务器的问题，换了服务器连接即解决
