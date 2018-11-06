#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import winshell
import logging
import shutil
import re
from configparser import ConfigParser
from time import sleep


def prepare_to_update():
    step_one = input("请确认已使用管理员权限运行 UpdateConfiguredIP.exe（y or n）：")
    if (step_one is not 'y'):
        exit(0)

def create_backup_dir(new_ip):
    desktop = winshell.desktop()
    dir_path = os.path.join(desktop, "bkp%s" % new_ip)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path.join('\\')

def check_and_backup(func):
    def wrapper(*args, **kw):
        file_path, bkp_dir = args[0], args[1]
        logging.info('')
        if not os.path.exists(file_path):
            logging.info("%s doesn't exist" % file_path)
            return
        basename = os.path.basename(file_path)
        shutil.copy(file_path, bkp_dir + basename)
        logging.info('backup %s ...' % file_path)
        return func(*args, **kw)

    return wrapper

@check_and_backup
def change_ip(file_path, bkp_dir, new_ip):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    logging.info('substitute %s ...' % file_path)
    pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(file_path, 'w') as file:
        for line in lines:
            matchObj = re.search(pattern, line, re.M | re.I)
            if matchObj:
                logging.info("old text: %s" % line.strip('\n'))
                line = re.sub(pattern, new_ip, line)
                logging.info("new text: %s" % line.strip('\n'))
            file.write(line)

@check_and_backup
def UpdateINI(config_file_path, bkp_dir, new_ip):
    def set_and_print_cfg_value(section, option):
        old_value = cfg.get(section, option)
        pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        matchObj = re.search(pattern, old_value, re.M | re.I)
        if matchObj:
            logging.info('old value: [%s]\t%s=%s', section, option, old_value)
            new_value = re.sub(pattern, new_ip, old_value)
            logging.info('new value: [%s]\t%s=%s', section, option, new_value)
            cfg.set(section, option, new_value)

    cfg = ConfigParser()
    cfg.read(config_file_path)
    logging.info('substitute %s ...' % config_file_path)
    set_and_print_cfg_value('INI_SECTION', 'INI_ITEM')

    with open(config_file_path, 'w') as file:
        cfg.write(file)

@check_and_backup
def ConsoleShortcut(link_file_path, bkp_dir, new_ip):
    logging.info('update %s ...' % link_file_path)
    with winshell.shortcut(link_file_path) as link:
        # link.path = 'C:\Program Files (x86)\Internet Explorer\iexplore.exe'
        # link.description = "Shortcut to python"
        old_value = link.arguments
        pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        matchObj = re.search(pattern, old_value, re.M | re.I)
        if matchObj:
            logging.info('old arguments: %s' % link.arguments)
            new_value = re.sub(pattern, new_ip, old_value)
            link.arguments = new_value
            logging.info('new arguments: %s' % link.arguments)


if __name__ == "__main__":
    prepare_to_update()
    new_ip = input("请输入新的 IP ：") or '192.168.1.1'
    bkp_dir = create_backup_dir(new_ip)

    logging.basicConfig(
        level=logging.DEBUG,
        format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename= "UpdateServerIP.log",
        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    home_dir = input("请输入待修改的文件所在目录路径 ：") or winshell.desktop()
    logging.debug(home_dir)
    change_ip(r'%stest.ini' % home_dir, bkp_dir, new_ip)
    link_file_desktop = r'C:\Users\Public\Desktop\ie_shortcut.lnk'
    ConsoleShortcut(link_file_desktop, bkp_dir, new_ip)
    sleep(10)
