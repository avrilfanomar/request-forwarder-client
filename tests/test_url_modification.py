import os
import unittest
from unittest.mock import patch
import sys
import urllib.parse

# Add the parent directory to sys.path to import the client module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.main import modify_url

class TestUrlModification(unittest.TestCase):
    """Test the URL modification functionality."""

    def test_no_modifications(self):
        """Test URL with no modifications."""
        url = "http://localhost:8080/api/v1/test?param=value"
        config = {
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        modified_url = modify_url(url, config)
        self.assertEqual(modified_url, url)

    def test_override_scheme(self):
        """Test overriding the scheme."""
        url = "http://localhost:8080/api/v1/test?param=value"
        config = {
            "scheme": "https",
            "redirect_url": None,
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        modified_url = modify_url(url, config)
        self.assertTrue(modified_url.startswith("https://"))
        self.assertIn("localhost:8080", modified_url)

    def test_override_port(self):
        """Test overriding the port."""
        url = "http://localhost:8080/api/v1/test?param=value"
        config = {
            "scheme": None,
            "redirect_url": None,
            "override_port": "9090",
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        modified_url = modify_url(url, config)
        self.assertIn("localhost:9090", modified_url)

    def test_override_path(self):
        """Test overriding the path."""
        url = "http://localhost:8080/api/v1/test?param=value"
        config = {
            "scheme": None,
            "redirect_url": None,
            "override_port": None,
            "override_path": "/new/path",
            "certificate_check_ignore": "false"
        }
        modified_url = modify_url(url, config)
        self.assertIn("/new/path", modified_url)
        self.assertIn("param=value", modified_url)

    def test_redirect_url(self):
        """Test redirecting to a different URL."""
        url = "http://localhost:8080/api/v1/test?param=value"
        config = {
            "scheme": None,
            "redirect_url": "https://newhost:9090",
            "override_port": None,
            "override_path": None,
            "certificate_check_ignore": "false"
        }
        modified_url = modify_url(url, config)
        self.assertTrue(modified_url.startswith("https://"))
        self.assertIn("newhost:9090", modified_url)
        self.assertIn("/api/v1/test", modified_url)

    def test_multiple_overrides(self):
        """Test multiple overrides at once."""
        url = "http://localhost:8080/api/v1/test?param=value"
        config = {
            "scheme": "https",
            "redirect_url": "http://newhost",
            "override_port": "9090",
            "override_path": "/new/path",
            "certificate_check_ignore": "false"
        }
        modified_url = modify_url(url, config)
        self.assertTrue(modified_url.startswith("https://"))
        self.assertIn("newhost:9090", modified_url)
        self.assertIn("/new/path", modified_url)
        self.assertIn("param=value", modified_url)

if __name__ == '__main__':
    unittest.main()
