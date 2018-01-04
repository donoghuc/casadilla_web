#!/bin/bash
ansible-playbook -vvvv ./init_config.yml --private-key='/home/cas/working_dir/casadilla_web/ssh/do_deploy' -u root -i ./hosts
