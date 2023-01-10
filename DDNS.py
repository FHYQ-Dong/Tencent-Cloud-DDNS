import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
from os.path import join
from getIP import getIPv6Address

# 读取同目录下的 SECRET, Domain 文件
def ReadFile(path:str):
    
    with open(join(path, "Secret"), mode="r", encoding="utf-8") as f:
        Secret = json.load(f)
    with open(join(path, "Domain"), mode="r", encoding="utf-8") as f:
        Domain = json.load(f)
    with open(join(path, "RecordSettings"), mode="r", encoding="utf-8") as f:
        RecordSettings = json.load(f)
    return Secret, Domain, RecordSettings

# 获取 RecordId
def GetRecordId(Domain:dict, Secret:dict) -> str :
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(Secret["Id"], Secret["Key"])
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.ap-beijing.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeRecordListRequest()
        params = {
            "Domain": Domain["Domain"]
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeRecordListResponse的实例，与请求对象对应
        resp = client.DescribeRecordList(req)
        for record in resp.RecordList:
            if record.Name == Domain["SubDomain"]:
                return record.RecordId
        # 输出json格式的字符串回包
        # print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)

# DDNS
def DDNS(Domain:dict, RecordSettings:dict, IP:str, Secret:dict):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(Secret["Id"], Secret["Key"])
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ModifyRecordRequest()
        params = {
            "Domain": Domain["Domain"],
            "SubDomain": Domain["SubDomain"],
            "RecordId": RecordId,
            "RecordType": RecordSettings["RecordType"],
            "RecordLine": RecordSettings["RecordLine"],
            "Value": IP
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
        resp = client.ModifyRecord(req)
        # 输出json格式的字符串回包
        # print(resp.to_json_string())
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        # print(err)
        return err

if __name__ == "__main__":
    Secret, Domain, RecordSettings = ReadFile(r"./")
    RecordId = GetRecordId(Domain, Secret)
    IP = getIPv6Address()
    res = DDNS(Domain, RecordSettings, IP, Secret)
    print(res)