import pytest
import os
from click.testing import CliRunner
from pulse.cli import main
from pulse.auth.manager import AuthManager

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Pulse" in result.output

def test_cli_auth_github_interactive(mocker):
    runner = CliRunner()
    # Mock the prompt
    mocker.patch('click.prompt', side_effect=['user', 'token'])
    
    with runner.isolated_filesystem() as td:
        mocker.patch.dict(os.environ, {"PULSE_HOME": td})
        result = runner.invoke(main, ['auth', 'github'])
        assert result.exit_code == 0
        assert "GitHub credentials saved" in result.output

def test_cli_github_no_auth(mocker):
    runner = CliRunner()
    # Ensure no auth exists
    with runner.isolated_filesystem() as td:
        mocker.patch.dict(os.environ, {"PULSE_HOME": td})
        result = runner.invoke(main, ['github'])
        assert "No credentials found" in result.output
