#!/usr/bin/python3
import configparser
import argparse
import sys
import os

CONFIG_PATH = os.path.expanduser('~/.ck2launcher')

parser = argparse.ArgumentParser(description=
    'Launcher for Crusader King II that allow to select mods and DLC')
parser.add_argument('-m', '--mods', nargs='*', help='Mods loaded')
parser.add_argument('-d', '--dlc', nargs='*', help='DLCs loaded')

def getConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    config_dict = {'ck2':{},'steam':{}}

    for section in config.sections():
        config_dict[section] = dict(config.items(section))

    return config_dict


def getArgs():
    return parser.parse_args()

def getOptions():
    config = getConfig()
    parser.set_defaults(**{
        'mods': config['ck2'].get('mods',''),
        'dlc': config['ck2'].get('dlc','')
    })
    args = getArgs()

    config['ck2']['mods'] = args.mods
    config['ck2']['dlc'] = args.dlc

    return config

def launchCk2():
    options = getOptions()



if __name__ == '__main__':
    launchCk2()
