# -*- coding: utf-8 -*-

import os.path

from yamlfred.utils import TemporaryDirectory

from yamlfred.alfred_workflow import AlfredWorkflow


def test_dump_plist():
    wf = AlfredWorkflow()
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'info.plist')
        wf.dump_plist(path)
        assert os.path.exists(path)


def test_dump_workflow():
    wf = AlfredWorkflow()
    with TemporaryDirectory() as tmpdir:
        default = {'path': 'workflow.yml', 'readme_path': 'README', 'script_dir': '.'}
        kwargs = {k: os.path.join(tmpdir, v) for k, v in default.items()}
        wf.dump_workflow(**kwargs)
        assert os.path.exists(kwargs['path'])

