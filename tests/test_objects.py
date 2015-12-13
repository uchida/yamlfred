# -*- coding: utf-8 -*-

from yamlfred.alfred_object import AlfredObject


def test_object_dump():
    dump = AlfredObject({"type": ""}).dump()
    assert dump["type"] == ""
