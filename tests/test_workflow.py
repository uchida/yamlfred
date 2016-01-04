# -*- coding: utf-8 -*-

import os.path

from testfixtures import TempDirectory

from yamlfred.utils import TemporaryDirectory

from yamlfred.alfred_workflow import AlfredWorkflow


def test_dump_empty_plist():
    wf = AlfredWorkflow()
    with TempDirectory() as d:
        path = os.path.join(d.path, 'info.plist')
        wf.dump_plist(path)
        assert os.path.exists(path)


def test_dump_empty_workflow():
    wf = AlfredWorkflow()
    with TempDirectory() as d:
        default = {'path': 'workflow.yml', 'readme_path': 'README', 'script_dir': '.'}
        kwargs = {k: os.path.join(d.path, v) for k, v in default.items()}
        wf.dump_workflow(**kwargs)
        assert os.path.exists(kwargs['path'])


def test_dump_gotcha_plist():
    wf = AlfredWorkflow()
    gotchas_dir = os.path.join(os.path.dirname(__file__), 'gotchas')
    wf.load_yaml(os.path.join(gotchas_dir, 'workflow.yml'))
    with TempDirectory() as d:
        path = os.path.join(d.path, 'info.plist')
        wf.dump_plist(path)
        d.compare(['info.plist'])


def test_dump_gotcha_workflow():
    wf = AlfredWorkflow()
    gotchas_dir = os.path.join(os.path.dirname(__file__), 'gotchas')
    wf.load_plist(os.path.join(gotchas_dir, 'info.plist'))
    with TempDirectory() as d:
        yml = os.path.join(d.path, 'workflow.yml')
        readme_path = os.path.join(d.path, 'README')
        wf.dump_workflow(path=yml, readme_path=readme_path, script_dir=d.path)
        gotchas = [ '17E27E05-02BA-489D-AC4A-CE170BFB245B',
                    '351ADB42-C9DB-42ED-B739-8FC5B698AB3F', 
                    '45CC4632-CC94-4B38-8081-9670DD843F62', 
                    '53766ED0-B222-4D67-9A22-F7C15CB2A4A1',
                    'README', 'workflow.yml', ]
        d.compare(gotchas)

