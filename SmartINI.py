#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import winreg
import os
import logging
import shutil
from configparser import ConfigParser
from xml.sax.handler import ContentHandler
from xml.sax import parse
from time import sleep


def prepare_to_update():
    step_one = input("请确认已使用管理员权限运行 SmartINI.exe（y or n）：")
    if (step_one is not 'y'):
        exit(0)

def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

def create_backup_dir():
    #desktop = get_desktop()
    desktop = os.curdir
    dir_path = os.path.join(desktop, "backup")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path + '\\'

class NewConfigParser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)
    def optionxform(self, optionstr):
        return optionstr

class IniHandler(ContentHandler):
    def __init__(self, bkp_dir):
        self.bkp_dir = bkp_dir
        self.valid = False
        self.file = ""
        self.section = ""
        self.key = ""
        self.value = ""
    def startElement(self, tag, attrs):
        if tag == 'File':
            self.file = attrs['Path']
            logging.info('')
            if not os.path.exists(self.file):
                logging.info("%s doesn't exist" % self.file)
                return
            basename = os.path.basename(self.file)
            shutil.copy(self.file, self.bkp_dir + basename)
            logging.info('backup %s successfully' % self.file)
        elif tag == 'AddKey' or tag == 'UpdateKey':
            self.valid = True
    def endElement(self, tag):
        if tag == 'AddKey' or tag == 'UpdateKey':
            self.valid = False
            cfg = NewConfigParser()
            logging.info(tag)
            cfg.read(self.file)
            cfg.set(self.section, self.key, self.value)
            logging.info('Update: [%s]\t%s=%s', self.section, self.key, self.value)
            with open(self.file, 'w') as file:
                cfg.write(file)
    def characters(self, content):
        if self.valid:
            logging.info(content)
            self.section, self.key, self.value = content.split(',')


if __name__ == "__main__":
    #prepare_to_update()
    bkp_dir = create_backup_dir()

    logging.basicConfig(
        level=logging.DEBUG,
        format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename= bkp_dir + "SmartINI.log",
        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.debug(bkp_dir)

    parse('SmartINI.xml', IniHandler(bkp_dir))

    sleep(3)