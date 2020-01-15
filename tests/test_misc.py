"""Miscellaneous tests for test coverage."""

from docoptcfg import docoptcfg
from tests import DOCSTRING_MULTI, EXPECTED_MULTI


def test_no_settable():
    """Test with all options overridden by command line."""
    actual = docoptcfg(DOCSTRING_MULTI, ['1', '--config=config.ini', '--flag', '--key=val'], env_prefix='MULTI_')
    expected = EXPECTED_MULTI.copy()
    expected['--config'] = 'config.ini'
    expected['--flag'] = 1
    expected['--key'] = ['val']
    assert actual == expected


def test_issue_7(monkeypatch, tmpdir):
    """Test to cover the issue [#7](https://github.com/Robpol86/docoptcfg/issues/7)"""

    docstring = """\
    Test to reproduce #7
    
    Usage:
        my_script [--key=VAL] [--env=ENV] [--config=FILE] <pos>...
        
    Options:
        --config=FILE  Path INI config file.
        --key=VAL      Key value [default: some_value]
        --env=ENV      Env value [default: some_env]
    """

    config_file = tmpdir.join('config.ini')
    config_file.write('[my_script]\nkey = another_value')

    expected = {
        '--config': str(config_file),
        '--key': 'another_value',
        '--env': 'another_env',
        '<pos>': ['1']
    }

    monkeypatch.setattr('sys.argv', ['my_script', '--config', str(config_file), '1'])
    monkeypatch.setenv('TEST_ENV', 'another_env')
    actual = docoptcfg(docstring, config_option='--config', env_prefix='TEST_')
    assert actual == expected
