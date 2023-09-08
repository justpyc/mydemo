支持存储类型：
    本地存储
    AWS-S3
    TENCETN-COS
python安装：
    要求版本：
        os版本：centos7.x or redhat7.x
        python3.8+
    1、可以使用python的 docker镜像 
    2、编译安装：
        yum install -y libffi zlib zlib-devel krb5-devel libtiff-devel \
        libjpeg-devel libzip-devel freetype-devel lcms2-devel \
        libwebp-devel tcl-devel tk-devel sshpass \
        openldap-devel openssh-clients telnet openldap-clients \
        libxml2 libxslt libffi-devel openssl-devel bzip2 bzip2-devel \
        ncurses ncurses-devel openssl openssl-devel openssl-static \
        zip.x86_64 libzip.x86_64 libzip-devel.x86_64  readline.x86_64 readline-devel.x86_64 \
        readline-static.x86_64 \
        make gcc gdbm-devel sqlite-devel libffi-devel tk-devel xz-devel

        python3.8安装
        ./configure --with-ensurepip
        
        安装虚拟环境：
        pip3 install virtualenv
        pip3 install virtualenv  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com 

        virtualenv py38
        cd py38 && source ./bin/activate
        pip3 install -r requirments.txt
        
初始化数据库：
python manage.py makemigrations
python manage.py migrate

运行服务
python manage.py runserver 0.0.0.0:8000
