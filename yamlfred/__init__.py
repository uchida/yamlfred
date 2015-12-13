# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys

# to evade UnicodeDecodeError on plistlib.writePlist
reload(sys)
sys.setdefaultencoding('utf-8')

import argparse
import shutil
import uuid
import os.path

import yaml

from yamlfred.utils import (
    unicode_representer, unicode_constructor,
    Include, include_representer, include_constructor,
)

yaml.add_representer(unicode, unicode_representer)
yaml.add_constructor("tag:yaml.org,2002:str", unicode_constructor)
yaml.add_representer(Include, include_representer)
yaml.add_constructor('!include', include_constructor)

import plistlib
from yamlfred.utils import translate_plist

from yamlfred.utils import TemporaryDirectory

from yamlfred.alfred_connections import AlfredConnections
from yamlfred.alfred_object import AlfredObject


class AlfredWorkflow(object):

    def __init__(self):
        self.readme = ""
        self.prop = {
            "name": str(uuid.uuid1()),
            "description": "",
            "bundleid": "",
            "createdby": "",
            "webaddress": ""
        }
        self.connections = []
        self.objects = []
        return

    def load_plist(self, path):
        plist = plistlib.readPlist(path)
        info = translate_plist(plist)
        self.readme = info.get("readme")
        for key in info.keys():
            self.prop[key] = info[key]
        for obj in info["objects"]:
            self.objects.append(AlfredObject(obj))
        self.connections = AlfredConnections(self.objects, info["connections"])
        return

    def load_yaml(self, path):
        with open(path, 'r') as f:
            s = f.read()
            wf_yaml = yaml.load(s.decode('utf8'))
        for key in wf_yaml.keys():
            self.prop[key] = wf_yaml[key]
        for obj in wf_yaml["objects"]:
            new_obj = {'uid': str(uuid.uuid1())}
            new_obj.update(obj)
            uid = new_obj['uid']
            if 'uidata' not in self.prop:
                self.prop['uidata'] = {}
            if uid not in self.prop['uidata']:
                cat = new_obj['type'].split('.')[3]
                uids = [o.prop['uid'] for o in self.objects if cat in o.type]
                if uids:
                    max_ypos = max(
                        self.prop['uidata'][u]['ypos'] for u in uids
                    )
                    self.prop['uidata'][uid] = {'ypos': max_ypos + 120}
                else:
                    self.prop['uidata'][uid] = {'ypos': 30}
            self.objects.append(AlfredObject(new_obj))
        self.connections = AlfredConnections(
            self.objects, wf_yaml["connections"]
        )
        return

    def dump_plist(self):
        dic = dict(self.prop.items())
        dic["objects"] = [obj.prop for obj in self.objects]
        dic["connections"] = self.connections.items
        plistlib.writePlist(dic, 'info.plist')
        return

    def dump_workflow(self):
        dic = dict(self.prop.items())
        dic["objects"] = [obj.dump() for obj in self.objects]
        dic["connections"] = self.connections.dump()
        if self.readme:
            with open('README', 'w') as f:
                f.write(self.readme.encode('utf-8'))
            dic['readme'] = Include('README')
        with open('workflow.yml', 'w') as f:
            yaml.dump(dic, f, default_flow_style=False)
        return


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A tool to manage Alfred Workflow via yaml templates",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers(help='commands')

    plist_parser = subparsers.add_parser(
        'to_yaml', help='convert plist into workflow.yml'
    )
    plist_parser.set_defaults(func=to_yaml)

    yaml_parser = subparsers.add_parser(
        'to_plist', help='convert yaml templates into info.plist'
    )
    yaml_parser.set_defaults(func=to_plist)

    extract_parser = subparsers.add_parser(
        'extract', help='extract Alfred workflow'
    )
    extract_parser.add_argument(
        'path', action='store', help='path to Alfred workflow'
    )
    extract_parser.set_defaults(func=extract)

    create_parser = subparsers.add_parser(
        'create', help='create Alfred workflow from workflow.yml'
    )
    create_parser.add_argument(
        'name', action='store', help='name of Alfred workflow'
    )
    create_parser.set_defaults(func=create)
    return parser.parse_args()


def to_yaml(args):
    wf = AlfredWorkflow()
    wf.load_plist('info.plist')
    wf.dump_workflow()
    return


def to_plist(args):
    wf = AlfredWorkflow()
    wf.load_yaml('workflow.yml')
    wf.dump_plist()
    return


def extract(args):
    import zipfile
    with zipfile.ZipFile(args.path, "r", zipfile.ZIP_DEFLATED) as zip:
        extract_path = os.path.splitext(args.path)[0]
        zip.extractall(path=extract_path)
    return


def create(args):
    wf = AlfredWorkflow()
    wf.load_yaml('workflow.yml')
    wf.dump_plist()
    # copy to tmpdir
    with TemporaryDirectory() as tmpdir:
        tmppath = os.path.join(tmpdir, args.name)
        shutil.copytree(os.path.curdir, tmppath)
        name = shutil.make_archive(args.name, 'zip', tmppath)
        shutil.move('{}.zip'.format(args.name),
                    '{}.alfredworkflow'.format(args.name))
    return


def main():
    args = parse_arguments()
    args.func(args)
    sys.exit(0)
