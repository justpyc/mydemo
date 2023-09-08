import os
# from concurrent.futures import ProcessPoolExecutor
from django.http import JsonResponse
from django.shortcuts import render, redirect

from mydemo.settings import FILE_INTPUT_PATH, FILE_OUTPUT_PATH
from myapp.models import Storage
from myapp.utils import is_file_execute, Handlers, handler_execute_file

# executor = ProcessPoolExecutor(30)

def upload_file(request):
    # pprint(request.POST.dict())
    data = request.POST.dict()
    filename = data.get("name", "random.file")
    storage_type = int(data.get("storage_type", 0))
    # file_name = request.FILES
    # size = request.FILES.size
    # print(request.FILES)
    stream = request.FILES["file"]
    # name = request.FILES["name"]
    file_path = os.path.join(FILE_INTPUT_PATH, filename)
    print("file path:{p}".format(p=file_path))
    is_execute = is_file_execute(file_path)
    if Handlers.get(storage_type):
        Handlers[storage_type](file_path, stream)
    else:
        return set_status_4xx(403, message="stroage type error:{s}".format(s=storage_type))
    p = Storage(**{
        "storage_type": storage_type,
        "input_path": file_path,
        "is_executable":is_execute
        }
    )
    p.save()
    print("upload file :{p} success".format(p=file_path))
    return set_status_2xx(data={"path":file_path})

def execute_file(request):
    data = request.POST.dict()
    storage_id = data.get("storage_id")
    filename = data.get("filename")
    output_path = os.path.join(FILE_OUTPUT_PATH, os.path.basename(filename))
    print("create output path:{p}".format(p=output_path))
    handler_execute_file(storage_id, output_path)
    return set_status_2xx(data="success")


def index(request):
    return render(request, "index.html")


def list_files(request):
    o = Storage.objects.all()
    context = {"record": o}
    return render(request, "list_files.html", context)

def set_status_4xx(code=400, message='client error', data=None):
    if data is None:
        return JsonResponse({"code": code, "message": message}, status=code)
    else:
        return JsonResponse({
            "code": code, "message": message, "data": data}, status=code
        )


def set_status_5xx(code=500, message='server runtime error', data=None):
    if data is None:
        return JsonResponse({"code": code, "message": message}, status=code)
    else:
        return JsonResponse({
            "code": code, "message": message, "data": data}, status=code
        )

def set_status_2xx(data, code=200, message='success'):
    return JsonResponse({
        "code": code, "message": message, "data": data
    }, status=code)
