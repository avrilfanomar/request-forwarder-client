import os
import unittest
from unittest.mock import patch, MagicMock
import sys
import subprocess

# Add the parent directory to sys.path to import the client module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.main import execute_command

class TestCommandExecution(unittest.TestCase):
    """Test the command execution functionality."""

    @patch('subprocess.run')
    def test_simple_command(self, mock_run):
        """Test executing a simple command."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        mock_run.return_value = MagicMock(stdout="test output")
        execute_command("echo test", config)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], ['echo', 'test'])

    @patch('subprocess.run')
    def test_command_with_url(self, mock_run):
        """Test executing a command with a URL."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        mock_run.return_value = MagicMock(stdout="test output")
        execute_command("curl http://localhost:8080/api/v1/test", config)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], ['curl', 'http://localhost:8080/api/v1/test'])

    @patch('subprocess.run')
    def test_command_with_invalid_url_host(self, mock_run):
        """Test executing a command with an invalid URL host."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        execute_command("curl http://example.com/api/v1/test", config)
        mock_run.assert_not_called()

    @patch('subprocess.run')
    def test_command_with_url_and_certificate_ignore(self, mock_run):
        """Test executing a command with a URL and certificate check ignore."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "true"
        }
        mock_run.return_value = MagicMock(stdout="test output")
        execute_command("curl http://localhost:8080/api/v1/test", config)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], ['curl', 'http://localhost:8080/api/v1/test', '-k'])

    @patch('subprocess.run')
    def test_command_with_url_and_override_port(self, mock_run):
        """Test executing a command with a URL and override port."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": "9090",
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        mock_run.return_value = MagicMock(stdout="test output")
        execute_command("curl http://localhost:8080/api/v1/test", config)
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], ['curl', 'http://localhost:9090/api/v1/test'])

    @patch('subprocess.run')
    def test_command_error(self, mock_run):
        """Test executing a command that results in an error."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        mock_run.side_effect = subprocess.CalledProcessError(1, "test", stderr="test error")
        execute_command("invalid_command", config)
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
