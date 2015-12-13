# -*- coding: utf-8 -*-

from yamlfred.alfred_connections import AlfredConnections


def test_connection_dump():
    objects = []
    connections = {}
    dump = AlfredConnections(objects, connections).dump()
    assert dump == {}
