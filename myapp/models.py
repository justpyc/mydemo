from django.db import models


StorageType = (
    (0, 'LocalStorage'),
    (1, 'S3'),
    (2, 'Tencent-COS'),
)

class Storage(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="ID")
    storage_type = models.IntegerField(choices=StorageType, default=0, verbose_name="存储类型")
    input_path = models.CharField(max_length=64, verbose_name='上传路径')
    is_executable = models.BooleanField(default=False, verbose_name='是否可执行')
    output_path = models.TextField(verbose_name='输出结果保存路径',default="")    

    class Meta:
        db_table = 'storage'
