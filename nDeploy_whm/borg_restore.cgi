#!/usr/bin/env python

import commoninclude
import cgitb
import subprocess
import cgi
import os
import yaml
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()
form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('action') and os.path.isfile(borgmatic_config_file):

    # We will retrive the borg repo details from borgmatic config
    # Get all config settings from the borgmatic config file
    with open(borgmatic_config_file, 'r') as borgmatic_config_file_stream:
        yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_config_file_stream)
    borg_repo = yaml_parsed_borgmaticyaml['location']['repositories'][0]
    encryption_passphrase = yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']
    my_env = os.environ.copy()
    my_env["BORG_PASSPHRASE"] = encryption_passphrase
    my_env["LANG"] = 'en_US.UTF-8'
    if form.getvalue('action') == 'umount':

        the_raw_cmd_orig = 'borg umount /root/borg_restore_point >> '+whm_terminal_log
        the_raw_cmd = the_raw_cmd_orig.decode('utf-8')

        procExe = subprocess.Popen('echo -e "Unmounting restore point..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(the_raw_cmd, env=my_env, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo -e "Restore point unmounted..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Restore Point Unmounted!')

    elif form.getvalue('action') == 'mount':
        if form.getvalue('restorepoint'):
            restore_point_dict = {'restore_point': form.getvalue('restorepoint')}
            with open('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE', 'w') as restore_point_conf:
                yaml.dump(restore_point_dict, restore_point_conf, default_flow_style=False)

            the_raw_cmd_orig = 'borg mount '+borg_repo+'::'+form.getvalue('restorepoint')+' /root/borg_restore_point >> '+whm_terminal_log
            the_raw_cmd = the_raw_cmd_orig.decode('utf-8')

            procExe = subprocess.Popen('echo -e "Mounting restore point: '+form.getvalue('restorepoint')+'" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen(the_raw_cmd, env=my_env, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('echo -e "Restore point '+form.getvalue('restorepoint')+' mounted..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
    
            commoninclude.print_success('Restore Point Mounted!')

        else:
            commoninclude.print_forbidden()
            print_simple_footer()
            exit(0)
    else:
        commoninclude.print_forbidden()
        print_simple_footer()
        exit(0)

else:
    commoninclude.print_forbidden()
print_simple_footer()
