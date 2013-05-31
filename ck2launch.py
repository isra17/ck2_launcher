#!/usr/bin/python3
import configparser
import argparse
import sys
import os

CONFIG_PATH = ['.ck2launcher', os.path.expanduser('~/.ck2launcher')]

parser = argparse.ArgumentParser(description=
    'Launcher for Crusader King II that allow to select mods and DLC')
parser.add_argument('-m', '--mods', nargs='*', help='Mods loaded')
parser.add_argument('-d', '--exclude-dlc', nargs='*', help='DLCs excluded')

def getConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    config_dict = {
        'ck2':{
            'mods':[],
            'exclude_dlc':[]
        },
        'steam':{}
    }

    config_dict['steam'] = dict(config.items('steam'))
    if config.has_option('ck2', 'exclude_dlc'):
        config_dict['ck2']['exclude_dlc'] = \
            config.get('ck2','exclude_dlc').split('\n')

    if config.has_option('ck2', 'mods'):
        config_dict['ck2']['mods'] = \
            config.get('ck2','mods').split('\n')


    return config_dict


def getArgs():
    return parser.parse_args()

def getOptions():
    config = getConfig()
    parser.set_defaults(**{
        'mods': config['ck2'].get('mods',[]),
        'exclude_dlc': config['ck2'].get('exclude_dlc',[])
    })
    args = getArgs()

    config['ck2']['mods'] = args.mods
    config['ck2']['exclude_dlc'] = args.exclude_dlc

    return config

def launchck2(options):
    ck2_path = os.path.expanduser(options['steam']['ck2_bin'])
    args = [ck2_path]
    args.extend(list(map(lambda mod: '-mod=mod/' + mod,
            options['ck2']['mods'])))
    args.extend(list(map(lambda dlc: '-exculde_dlc=dlc/' + dlc,
            options['ck2']['exclude_dlc'])))

    os.execvp(ck2_path, args)

def main():
    options = getOptions()
    launchck2(options)


if __name__ == '__main__':
    main()
