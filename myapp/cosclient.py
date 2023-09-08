#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import string

from myapp.qcloud_cos import CosConfig
from myapp.qcloud_cos import CosS3Client
from myapp.qcloud_cos.cos_comm import format_endpoint
# from qcloud_cos import CosServiceError
# from qcloud_cos import CosClientError


class CosClient(object):
    def __init__(self, secret_key, secret_id, region, appid, end_point=None, scheme="http"):
        self.region = region
        self.appid = appid
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.end_point = end_point
        self.scheme = scheme
        self.cos_config = CosConfig(
            Secret_id=self.secret_id,
            Secret_key=self.secret_key,
            Endpoint=format_endpoint(self.end_point, self.region),
            Scheme=self.scheme)
        self.client = CosS3Client(self.cos_config)

    def create_bucket(self, bucket_name):
        # 创建存储桶
        self.client.create_bucket(Bucket=bucket_name + '-' + self.appid)
        return 0

    def create_bucket_with_ACL(self, bucket_name, acl):
        # 创建存储桶 ACL
        self.client.create_bucket(
            Bucket=bucket_name + '-' + self.appid, ACL=acl)
        return 0

    def create_bucket_with_GrantFullControl(self, bucket_name, owner_uin,
                                            sub_uin):
        # 创建存储桶 GrantFullControl
        grant_full_control = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin,
                                                               sub_uin)
        self.client.create_bucket(
            Bucket=bucket_name + '-' + self.appid,
            GrantFullControl=grant_full_control)
        return 0

    def create_bucket_with_GrantRead(self, bucket_name, owner_uin, sub_uin):
        # 创建存储桶 GrantRead
        grant_read = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin, sub_uin)
        self.client.create_bucket(
            Bucket=bucket_name + '-' + self.appid, GrantRead=grant_read)
        return 0

    def create_bucket_with_GrantWrite(self, bucket_name, owner_uin, sub_uin):
        # 创建存储桶 GrantRead
        grant_write = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin, sub_uin)
        self.client.create_bucket(
            Bucket=bucket_name + '-' + self.appid, GrantRead=grant_write)
        return 0

    def delete_bucket(self, bucket_name):
        # 删除存储桶
        self.client.delete_bucket(Bucket=bucket_name + '-' + self.appid)
        return 0

    def head_bucket(self, bucket_name):
        # 判断存储桶是否存在
        self.client.head_bucket(Bucket=bucket_name + '-' + self.appid)
        return 0

    def get_bucket_location(self, bucket_name):
        # 获取存储桶地域信息
        resp = self.client.get_bucket_location(Bucket=bucket_name + '-' + self.appid)
        return resp["LocationConstraint"]

    def list_objects(self, bucket_name):
        # 获取存储桶下文件列表
        resp = self.client.list_objects(Bucket=bucket_name + '-' + self.appid)
        return resp

    def list_objects_with_prefix(self, bucket_name, prefix):
        # 获取存储桶下有prefix前缀的文件列表
        resp = self.client.list_objects(
            Bucket=bucket_name + '-' + self.appid, Prefix=prefix)
        return resp

    def list_objects_with_delimiter(self, bucket_name, delimiter):
        # 模拟文件夹结构获取存储桶下 的文件列表
        resp = self.client.list_objects(
            Bucket=bucket_name + '-' + self.appid, Delimiter=delimiter)
        return resp

    def list_objects_with_Marker(self, bucket_name, marker):
        # 获取存储桶下文件名包含marker的文件列表
        resp = self.client.list_objects(
            Bucket=bucket_name + '-' + self.appid, Marker=marker)
        return resp

    def list_objects_with_Maxkeys(self, bucket_name, maxkeys):
        # 获取存储桶下最多maxkeys个文件列表
        resp = self.client.list_objects(
            Bucket=bucket_name + '-' + self.appid, MaxKeys=maxkeys)
        return resp

    def put_bucket_acl(self, bucket_name, acl):
        # 设置存储桶访问控制权限 ACL
        self.client.put_bucket_acl(
            Bucket=bucket_name + '-' + self.appid, ACL=acl)
        return 0

    def put_bucket_acl_with_GrantFullControl(self, bucket_name, owner_uin,
                                             sub_uin):
        # 设置存储桶访问控制权限 GrantFullControl
        grant_full_control = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin,
                                                               sub_uin)
        self.client.put_bucket_acl(
            Bucket=bucket_name + '-' + self.appid,
            GrantFullControl=grant_full_control)

    def put_bucket_acl_with_GrantRead(self, bucket_name, owner_uin, sub_uin):
        # 设置存储桶访问控制权限 GrantRead
        grant_read = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin, sub_uin)
        self.client.put_bucket_acl(
            Bucket=bucket_name + '-' + self.appid, GrantRead=grant_read)
        return 0

    def put_bucket_acl_with_GrantWrite(self, bucket_name, owner_uin, sub_uin):
        # 设置存储桶访问控制权限 GrantWrite
        grant_write = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin, sub_uin)
        self.client.put_bucket_acl(
            Bucket=bucket_name + '-' + self.appid, GrantRead=grant_write)

    def get_bucket_acl(self, bucket_name):
        # 获取存储桶访问控制权限
        resp = self.client.get_bucket_acl(Bucket=bucket_name + '-' + self.appid)
        return resp

    def put_bucket_cors(self, bucket_name, max_age_seconds=0):
        # 设置一条存储桶跨域访问规则
        corsconfig = {
            "CORSRule": [{
                "ID": "CORSRule 1",
                "MaxAgeSeconds": max_age_seconds,
                "AllowedOrigin": ["http://cloud.tencent.com"],
                "AllowedMethod": ["GET"]
            }]
        }
        self.client.put_bucket_cors(
            Bucket=bucket_name + '-' + self.appid,
            CORSConfiguration=corsconfig)
        return 0

    def put_bucket_multi_cors(self, bucket_name):
        # 设置多条存储桶跨域访问规则
        corsconfig = {
            "CORSRule": [{
                "ID": "CORSRule 1",
                "AllowedOrigin": ["http://cloud.tencent.com"],
                "AllowedMethod": ["GET"]
            }, {
                "ID": "CORSRule 2",
                "AllowedOrigin": ["http://cloud.tencent.com"],
                "AllowedMethod": ["POST"]
            }, {
                "ID": "CORSRule 3",
                "AllowedOrigin": ["http://cloud.tencent.com"],
                "AllowedMethod": ["PUT"]
            }]
        }
        self.client.put_bucket_cors(
            Bucket=bucket_name + '-' + self.appid,
            CORSConfiguration=corsconfig)
        return 0

    def get_bucket_cors(self, bucket_name):
        # 获取存储桶跨域访问规则
        resp = self.client.get_bucket_cors(Bucket=bucket_name + '-' + self.appid)
        return resp

    def delete_bucket_cors(self, bucket_name):
        # 删除存储桶跨域访问规则
        self.client.delete_bucket_cors(Bucket=bucket_name + '-' + self.appid)
        return 0

    def put_object_str(self, bucket_name, obj_name, str_len):
        # 上传字符串到对象
        self.client.put_object(
            Bucket=bucket_name + '-' + self.appid,
            Body="".join(
                random.choice(string.ascii_letters + string.digits)
                for i in range(str_len)),
            Key=obj_name)
        return 0

    def put_object_file(self, bucket_name, obj_name, file_name):
        # 上传文件到对象
        rsp = self.client.put_object(
            Bucket=bucket_name + '-' + self.appid,
            Body=open(file_name, "rb").read(),
            Key=obj_name)
        return rsp

    def head_object(self, bucket_name, obj_name):
        # 对象是否存在，获取对象属性
        resp = self.client.head_object(
            Bucket=bucket_name + '-' + self.appid, Key=obj_name)
        return resp

    def get_object(self, bucket_name, obj_name, file_name):
        # 下载对象
        resp = self.client.get_object(
            Bucket=bucket_name + '-' + self.appid, Key=obj_name)
        resp["Body"].get_stream_to_file(file_name)
        return resp

    def delete_object(self, bucket_name, obj_name):
        # 删除对象
        self.client.delete_object(
            Bucket=bucket_name + '-' + self.appid, Key=obj_name)
        return 0

    def delete_objects(self, bucket_name, obj_list):
        # 批量删除对象
        _obj = []
        for obj in obj_list:
            _obj.append({"Key": obj})
        delete = {
            "Object": _obj,
        }
        resp = self.client.delete_objects(
            Bucket=bucket_name + '-' + self.appid, Delete=delete)
        return resp

    def delete_objects_with_quiet(self, bucket_name, obj_list, quiet):
        # 批量删除对象
        _obj = []
        for obj in obj_list:
            _obj.append({"Key": obj})
        delete = {"Object": _obj, "Quiet": quiet}
        resp = self.client.delete_objects(
            Bucket=bucket_name + '-' + self.appid, Delete=delete)
        return resp

    def copy_object_in_same_bucket(self, obj, bucket_name, new_obj):
        # 桶内copy对象
        copy_source = {
            "Appid": self.appid,
            "Bucket": bucket_name,
            "Key": obj,
            "Region": self.region
        }
        resp = self.client.copy_object(
            Bucket=bucket_name + '-' + self.appid,
            Key=new_obj,
            CopySource=copy_source,
            CopyStatus="Copy")
        return resp

    def copy_object_in_different_bucket(self, obj, bucket_name, dst_bucket_name, dst_obj=None):
        copy_source = {
            "Appid": self.appid,
            "Bucket": bucket_name + '-' + self.appid,
            "Key": obj,
            "Region": self.region
        }
        if dst_obj is None:
            dst_obj = obj
        resp = self.client.copy_object(
            Bucket=dst_bucket_name,
            Key=dst_obj,
            CopySource=copy_source)
        return resp

    def put_object_acl(self, bucket_name, obj_name, acl):
        # 设置对象访问控制权限 ACL
        self.client.put_object_acl(
            Bucket=bucket_name + '-' + self.appid, Key=obj_name, ACL=acl)
        return 0

    def put_object_acl_with_GrantFullControl(self, bucket_name, obj_name,
                                             owner_uin, sub_uin):
        # 设置对象访问控制权限 GrantFullControl
        grant_full_control = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin,
                                                               sub_uin)
        self.client.put_object_acl(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            GrantFullControl=grant_full_control)

    def put_object_acl_with_GrantRead(self, bucket_name, obj_name, owner_uin,
                                      sub_uin):
        # 设置对象访问控制权限 GrantRead
        grant_read = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin, sub_uin)
        self.client.put_object_acl(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            GrantRead=grant_read)
        return 0

    def put_object_acl_with_GrantWrite(self, bucket_name, obj_name, owner_uin,
                                       sub_uin):
        # 设置对象访问控制权限 GrantWrite
        grant_write = 'id="qcs::cam::uin/%s:uin/%s"' % (owner_uin, sub_uin)
        self.client.put_object_acl(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            GrantWrite=grant_write)

    def get_object_acl(self, bucket_name, obj_name):
        # 获取对象访问控制权限
        resp = self.client.get_object_acl(
            Bucket=bucket_name + '-' + self.appid, Key=obj_name)
        return resp

    def create_multipart_upload(self, bucket_name, obj_name):
        # 创建分块上传
        resp = self.client.create_multipart_upload(
            Bucket=bucket_name + '-' + self.appid, Key=obj_name)
        return resp

    def abort_multipart_upload(self, bucket_name, obj_name, upload_id):
        # 放弃分块上传
        self.client.abort_multipart_upload(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            UploadId=upload_id)
        return 0

    def upload_part(self, bucket_name, obj_name, part_number, upload_id,
                    str_len):
        # 上传分块
        resp = self.client.upload_part(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            Body="".join(
                random.choice(string.ascii_letters + string.digits)
                for i in range(str_len)),
            PartNumber=part_number,
            UploadId=upload_id)
        return resp

    def list_parts(self, bucket_name, obj_name, upload_id):
        # 列出上传分块
        resp = self.client.list_parts(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            UploadId=upload_id)
        return resp

    def complete_multipart_upload(self, bucket_name, obj_name, upload_id,
                                  multipart_upload):
        # 完成分块上传
        resp = self.client.complete_multipart_upload(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            UploadId=upload_id,
            MultipartUpload=multipart_upload)
        return resp

    def list_multipart_uploads(self, bucket_name):
        resp = self.client.list_multipart_uploads(Bucket=bucket_name + '-' + self.appid)
        return resp

    def upload_file(self, bucket_name, obj_name, file_path):
        # 文件上传(断点续传)
        resp = self.client.upload_file(
            Bucket=bucket_name + '-' + self.appid,
            Key=obj_name,
            LocalFilePath=file_path)
        return resp


if __name__ == "__main__":
    from pprint import pprint
    import settings

    test = CosClient(secret_key=settings.CobraCOSSecretKey, secret_id=settings.CobraCOSSecretID,
                     region=settings.CobraCOSRegion, appid=settings.CobraCOSAppID)
    # result = test.list_objects(settings.CobraCOSBucket)
    # pprint(result)
    # rsp = test.upload_file(settings.CobraCOSBucket,
    #                        "node-v10.18.1.tar.gz",
    #                        "/root/node-v10.18.1.tar.gz")
    # rsp1 = test.put_object_file(settings.CobraCOSBucket, "business.json", "/root/business.json")
    # pprint(rsp1)
    # print(type(rsp1))
    # test.head_object()
    # rsp = test.get_object(settings.CobraCOSBucket,
    #                 "/TCE3.6.0/TCE3.6.0.T6864/x86/yaml/tcloud-dc-oss.1.6.14-20220125-174751-cb5783c.tgz",
    #                 "/mnt/test.tgz")
    # print(rsp)

