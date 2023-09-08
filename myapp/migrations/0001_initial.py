# Generated by Django 4.1.3 on 2023-09-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_type', models.IntegerField(choices=[(0, 'LocalStorage'), (1, 'S3'), (2, 'Tencent-COS')], default=0, verbose_name='存储类型')),
                ('input_path', models.CharField(max_length=64, verbose_name='上传路径')),
                ('is_executable', models.BooleanField(default=False, verbose_name='是否可执行')),
                ('output_path', models.TextField(verbose_name='输出结果保存路径')),
            ],
            options={
                'db_table': 'storage',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='用户ID')),
                ('username', models.CharField(max_length=64, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]