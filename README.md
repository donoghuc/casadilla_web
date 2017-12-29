# Personal Website Implemented Using Pyramid

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

## Install node and npm (for bower to manage static resources)
NOTE: for some reason npm only worked with elevated permission? should look in to a way around that. 
```
cas@ubuntu:~$ curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
cas@ubuntu:~$ sudo apt-get install nodejs
cas@ubuntu:~$ sudo npm install -g bower
```
## set up conda environment
```
cas@ubuntu:~$ conda create --name web_app
cas@ubuntu:~$ source activate web_app
(web_app) cas@ubuntu:~$ 
```
