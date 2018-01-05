# Personal Website Implemented Using Pyramid

This repository contians the source code for my personal website. 
[cas-donoghue.org](https://www.cas-donoghue.org)

## Build new ubuntu VM (VMware version: 12.5.7 build-5813279)
```
cas@ubuntu:~$ lsb_release -a
Distributor ID:	Ubuntu
Description:	Ubuntu 17.04
Release:	17.04
Codename:	zesty
```
## Install python via miniconda
```
# download miniconda
cas@ubuntu:~$ curl -LO https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
# install miniconda
cas@ubuntu:~$ bash Miniconda3-latest-Linux-x86_64.sh -p ~/miniconda -b
# add "export PATH=~/miniconda/bin:$PATH" to env variable
cas@ubuntu:~$ subl .bashrc
cas@ubuntu:~$ source .bashrc
cas@ubuntu:~$ python --version
Python 3.6.3 :: Anaconda, Inc.
```
## Project Dir
Note: I have this project at ~/working_dir/casadilla_web. This will be noted in file paths in examples below

## Make virtual environment for project
```
cas@ubuntu:~$ pip install virtualenv
cas@ubuntu:~/working_dir/casadilla_web$ virtualenv -p /home/cas/miniconda/bin/python web_app
cas@ubuntu:~/working_dir/casadilla_web$ source ./web_app/bin/activate
(web_app) cas@ubuntu:~/working_dir/casadilla_web$ 

```

## Install node and npm (for bower to manage static resources)
NOTE: for some reason npm only worked with elevated permission? should look in to a way around that. 
```
cas@ubuntu:~$ curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
cas@ubuntu:~$ sudo apt-get install nodejs
cas@ubuntu:~$ sudo npm install -g bower
```
## use bower to get static resources
```
(web_app) cas@ubuntu:~/working_dir/casadilla_web/casadilla_app/static$ bower install bootstrap-css jquery-dist respond html5shiv font-awesome
```
## build project package
```
(web_app) cas@ubuntu:~/working_dir/casadilla_web$ pip install -e .
```

## start development server on local machine
```
(web_app) cas@ubuntu:~/working_dir/casadilla_web$ pserve development.ini 
...TON OF LOGGIN STUFF OMMITED...
Running in dev mode.
Starting server in PID 8242.
Serving on http://localhost:6543
```
