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
parser.add_argument('--list-mods', action='store_true', help='List mods')
parser.add_argument('--list-dlc', action='store_true', help='List DLCs')

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

    return (config, args)

def launchck2(options):
    ck2_path = os.path.expanduser(options['steam']['ck2_bin'])
    args = [ck2_path]
    args.extend(list(map(lambda mod: '-mod=mod/' + mod,
            options['ck2']['mods'])))
    args.extend(list(map(lambda dlc: '-exclude_dlc=dlc/' + dlc,
            options['ck2']['exclude_dlc'])))

    print('Launch ck2 with options:')
    print(args)
    os.execvp(ck2_path, args)

def getName(iniFile):
    f = open(iniFile)
    for line in f.readlines():
        sline = line.split('=')
        if len(sline) == 2 and sline[0].strip() == 'name':
            return sline[1].strip()

def list_el(folder, extension):
    print("[Name]\t\t[Description]")
    folder = os.path.expanduser(folder)
    for f in os.listdir(folder):
        if f.endswith(extension):
            name = getName(folder + '/' + f)
            print('"' + f + '":\t' + name)

def list_mods(options):
    print('Mods:')
    list_el(options['steam']['ck2_user'] + '/mod', '.mod')

def list_dlc(options):
    print('DLCs:')
    list_el(options['steam']['ck2_path'] + '/dlc', '.dlc')

def main():
    options, args = getOptions()
    if args.list_mods:
        list_mods(options)
    elif args.list_dlc:
        list_dlc(options)
    else:
        launchck2(options)


if __name__ == '__main__':
    main()
