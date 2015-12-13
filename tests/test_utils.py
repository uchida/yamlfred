# -*- coding: utf-8 -*-

import os.path

import pytest

from yamlfred.utils import merge_dicts, remove_default, TemporaryDirectory


def test_merge_dicts():
    merged = merge_dicts({'foo': 'bar'}, {})
    assert merged['foo'] == 'bar'

    merged = merge_dicts({'foo': 'bar'}, {'foo': 'baz'})
    assert merged['foo'] == 'baz'

    merged = merge_dicts({'foo': 'bar'}, {'bar': 'baz'})
    assert merged['foo'] == 'bar'
    assert merged['bar'] == 'baz'

    merged = merge_dicts({'foo': {'bar': 'baz'}}, {})
    assert merged['foo']['bar'] == 'baz'

    merged = merge_dicts({'foo': {'bar': 'baz'}}, {'foo': {'bar': 'foobar'}})
    assert merged['foo']['bar'] == 'foobar'


def test_remove_default():
    removed = remove_default({'foo': 'bar'}, {})
    assert removed['foo'] == 'bar'

    removed = remove_default({'foo': 'bar'}, {'foo': 'bar'})
    assert 'foo' not in removed

    removed = remove_default({'foo': 'bar'}, {'foo': 'baz'})
    assert removed['foo'] == 'bar'

    removed = remove_default({'foo': {'bar': 'baz'}}, {'foo': {'bar': 'foobar'}})
    assert removed['foo']['bar'] == 'baz'

    removed = remove_default({'foo': {'bar': 'baz'}}, {'foo': {'bar': 'baz'}})
    assert 'foo' in removed
    assert 'bar' not in removed['foo']


def test_temporary_directory():
    tmppath = ''
    with TemporaryDirectory() as tmpdir:
        tmppath = tmpdir
        assert os.path.exists(tmppath), "temporal directory exists in with block"
    assert not os.path.exists(tmppath), "temporal directory absent out of block"
