#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from myapp.models import Storage
from myapp.cosclient import CosClient
from myapp.s3client import S3Client
from mydemo.settings import (
    COS_SECRET_KEY, COS_APP_ID, COS_BUCKET, COS_REGION, COS_SECRET_ID, FILE_OUTPUT_PATH
    )


def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj

def byte_to_str(o):
    if isinstance(o, bytes):
        return str(o, encoding="utf-8")
    elif isinstance(o, str):
        return o
    else:
        raise TypeError(str(type(o)))

def string_to_bytes(o):
    if isinstance(o, str):
        return bytes(o,encoding="utf-8")
    elif isinstance(o, bytes):
        return o
    else:
        raise TypeError(str(type(o)))


def is_file_execute(path):
    return os.access(path, os.X_OK) or str(path).endswith("sh")
    

def execute_file(path, output_path):
    if os.access(path, os.X_OK):
        cmd = "./{i} >>{o}".format(i=path, o=output_path)
    if str(path).endswith("sh"):
        cmd = "bash {i} >>{o}".format(i=path, o=output_path)
    os.system(cmd)
    return output_path

def handler_execute_file(storage_id, output_path):
    o = get_object_or_none(Storage, **{"id": storage_id})
    if o.is_executable:
        output_path = (output_path + ".out" )
        execute_file(o.input_path, output_path)
        if o.storage_type == 0:
            o.output_path = output_path
        elif o.storage_type == 1:
            download_path = os.path.join(FILE_OUTPUT_PATH, os.path.basename(o.input_path))
            S3Client().download_file(o.input_path, download_path)
            s3_output_path = "/{name}.out".format(name=os.path.basename(o.input_path))
            S3Client().upload_file(output_path, s3_output_path)
            o.output_path = s3_output_path
        elif o.storage_type == 2:
            download_path = os.path.join(FILE_OUTPUT_PATH, os.path.basename(o.input_path))
            COSHandler().download_file(o.input_path, download_path)
            cos_output_path = "/{name}.out".format(name=os.path.basename(o.input_path))
            COSHandler().upload_file(output_path, cos_output_path)
            o.output_path = cos_output_path
        o.save()
    

def handler_local_storage(path, f):
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def handler_cos_strage(path, f):
    handler_local_storage(path, f)
    return COSHandler().upload_file(path)


def handler_s3_strage(path, f):
    handler_local_storage(path, f)
    return S3Client().upload_file(path)


class COSHandler(object):
    def __init__(self) -> None:
        self.handler = CosClient(
            secret_key=COS_SECRET_KEY, secret_id=COS_SECRET_ID,
            region=COS_REGION, appid=COS_APP_ID
            )
    
    def upload_file(self, path, object_name=None):
        if object_name is None:
            object_name = os.path.join("/", os.path.basename(object_name))
        rsp = self.handler.upload_file(COS_BUCKET, object_name, path)
        print(rsp)
        return object_name
    
    def download_file(self, object_name, download_path):
        self.handler.get_object(COS_BUCKET, object_name, download_path)
        return download_path


Handlers = {
    0: handler_local_storage,
    1: handler_s3_strage,
    2: handler_cos_strage,
}

    

    