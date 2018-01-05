# Provision New Server
Rent a VPS (Ubuntu 16.04.03 x64). Use Ansible to configure following security features:
- dissalow root ssh login
- enable fail2ban (reject malicious IPs)
- set up non-root user

### Description (init_config)
```
deploy             :store all ansible related deployment source
|-group_vars       :store variable
|  |-all           :all variables in here (obviously not checked in to github)
|-roles            :ansible expects this structure
| |-init_config    :init config structure
|   |-tasks        :ansible instructions
|     |-main.yml   :this is the template for work to be completed to initialize new server
|-README           :this
|-hosts            :server IPs to provision (not checked in to github)
|-init.sh          :shell script to kick off ansible task so i dont have to remember command...
|-init_config.yml  :ansible playbook for initializing new server
```
### Outcome
__Note:__ variable names from deploy/roles/tasks/main.yml shown in [brackets] and [###] used to obscure sensitive info
1. group added to /etc/group ([deploy_group]: x :[###]:)
2. user added to /etc/passwd ([deploy_user]: x :[###]:[###]::/home/[deploy_user]:/bin/bash)
3. group added to /etc/sudoers (%[deploy_group] ALL=(ALL) NOPASSWD: ALL)
4. following params set in /etc/sshd_config:
 - PasswordAuthentication no (__Note:__ default setting was allready no for Ubuntu distro)
 - PermitRootLogin no

### Test
Can I log in as new user? :white_check_mark:
```
cas@ubuntu:~/working_dir/casadilla_web$ ssh -i /path/to/ssh/key [deploy_user]@[server ip]
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-104-generic x86_64)
```
Can I not log in as root? :white_check_mark:
```
cas@ubuntu:~/working_dir/casadilla_web$ ssh -i /path/to/ssh/key [deploy_user]@[server ip]
Permission denied (publickey).
```

# Push to production
In general: once server is provisioned (only happens once when it is brand new) automatically push updates to production from local dev env. 
### Work flow
1. run deploy playbook (stop server, pull updates from github, refresh and restart all services)
2. make changes on local laptop (test in dev and prod mode)
3. push changes to github
4. GOTO 1

### Description (deploy)
```
deploy                          :store all ansible related deployment source
|-group_vars                    :store variable
|  |-all                        :all variables in here (obviously not checked in to github)
|-roles                         :ansible instructions
| |-common                      :common tasks (not init_config)
|   |-handlers                  :deal with services (nginx)
|     |-main.yml                :define restart nginx
|   |-tasks                     :ansible instructions
|     |-dependencies.yml        :handles app dependencies and virtualenv
|     |-git.yml                 :clones or pulls from git repo
|     |-letsencrypt.yml         :install lets encrypt and nginx, manages ssl
|     |-main.yml                :simply calls the other definitions in this dir in logical order
|     |-nginx.yml               :configure nginx reverse proxy and https
|     |-ubuntu.yml              :maintain apt dependencies and sets up firewall 
|     |-wsgi.yml                :use supervisor to keep waitress/pyramid running
|   |-templates                 :jinja templates for ansible
|     |-nginx_ssl.conf.j2       :configuration template for nginx
|     |-supervisor_app.conf.j2  :template for controlling supervisor
|-README                        :this
|-hosts                         :server IPs to provision (not checked in to github)
|-deploy.yml                    :playbook to direct deploy to production server
|-prod_deploy.sh                :has command to start the deployment (not checked in bc it has username)
```
__NOTES:__ 
1. rsa key pair generated on local machine, private key is copied to server, public key added to git repo with pull access only
2. contents of prod_deploy.sh generalized as follows
```
ansible-playbook -vvvv ./deploy.yml --private-key='/home/cas/working_dir/casadilla_web/ssh/do_deploy' -u [deploy user] -i ./hosts

