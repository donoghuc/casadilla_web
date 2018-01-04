# Provision New Server
Rent a VPS (Ubuntu 16.04.03 x64). Use Ansible to configure following security features:
- dissalow root ssh login
- enable fail2ban (reject malicious IPs)
- set up non-root user

### Description
```
deploy             :store all ansible related deployment source
|-group_vars       :store variable
|  |-all           :all variables in here (obviously not checked in to github)
|-roles            :ansible instructions
| |-tasks          :ansible expects
|   |-main.yml     :this is the template for work to be completed to initialize new server
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

