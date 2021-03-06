#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor


def ansible_play(war_path):
    variable_manager = VariableManager()
    loader = DataLoader()

    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list='/etc/ansible/hosts'
                          )
    playbook_path = '/opt/deploy_xk.yml'

    if not os.path.exists(playbook_path):
        print '[INFO] The playbook does not exist'
        sys.exit()

    Options = namedtuple('Options',
                         ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                          'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                          'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                      module_path=None, forks=100, remote_user='root', private_key_file=None, ssh_common_args=None,
                      ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False, become_method=None,
                      become_user='root', verbosity=None, check=False)

    variable_manager.extra_vars = {'target_hosts': 'deploy_host',
                                   'war_path': war_path}  # This can accomodate various other command line arguments.`

    passwords = {}

    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                            loader=loader, options=options, passwords=passwords)

    results = pbex.run()

if __name__ == '__main__':
    ansible_play()
