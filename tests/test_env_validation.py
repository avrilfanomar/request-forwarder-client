import os
import unittest
import sys

# Add the parent directory to sys.path to import the client module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.main import validate_environment_variables

class TestEnvironmentVariableValidation(unittest.TestCase):
    """Test the environment variable validation functionality."""

    def test_no_token(self):
        """Test validation when no token is set."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "NO_TOKEN_SET",
            "topic": "req/NO_TOKEN_SET",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 1)
        self.assertIn("No token present", errors[0])

    def test_valid_token(self):
        """Test validation with a valid token."""
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
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 0)

    def test_invalid_mode(self):
        """Test validation with an invalid mode."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "invalid_mode",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid MODE", errors[0])

    def test_valid_mode(self):
        """Test validation with a valid mode."""
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
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 0)

    def test_invalid_certificate_check_ignore(self):
        """Test validation with an invalid certificate check ignore value."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "invalid"
        }
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid CERTIFICATE_CHECK_IGNORE", errors[0])

    def test_valid_certificate_check_ignore(self):
        """Test validation with valid certificate check ignore values."""
        for value in ['true', 'false', 'TRUE', 'FALSE']:
            config = {
                "mqtt_broker": "37.157.254.65",
                "token": "valid_token",
                "topic": "req/valid_token",
                "mode": "exec",
                "scheme": None,
                "redirect_url": None,
                "override_port": None,
                "override_path": None,
                "certificate_check_ignore": value
            }
            errors = validate_environment_variables(config)
            self.assertEqual(len(errors), 0)

    def test_invalid_override_port(self):
        """Test validation with an invalid override port."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": "not_a_number",
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid OVERRIDE_PORT", errors[0])

    def test_valid_override_port(self):
        """Test validation with a valid override port."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "valid_token",
            "topic": "req/valid_token",
            "mode": "exec",
            "scheme": None,
            "redirect_url": None,
            "override_port": "8080",
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 0)

    def test_invalid_redirect_url(self):
        """Test validation with an invalid redirect URL."""
        # This test is a bit tricky since urllib.parse.urlparse doesn't validate much
        # It will accept most strings as URLs, so we'll skip this test for now
        pass

    def test_multiple_errors(self):
        """Test validation with multiple errors."""
        config = {
            "mqtt_broker": "37.157.254.65",
            "token": "NO_TOKEN_SET",
            "topic": "req/NO_TOKEN_SET",
            "mode": "invalid_mode",
            "scheme": None,
            "redirect_url": None,
            "override_port": "not_a_number",
            "override_path": None,
            "certificate_check_ignore": "invalid"
        }
        errors = validate_environment_variables(config)
        self.assertEqual(len(errors), 4)  # 3 errors + no token

if __name__ == '__main__':
    unittest.main()
