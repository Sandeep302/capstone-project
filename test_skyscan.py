import unittest
from unittest.mock import patch, Mock

from main import validate_city_input, get_coordinates, fetch_air_quality


class TestSkyScan(unittest.TestCase):

    # PASS 1
    def test_validate_city_input_valid(self):
        valid, msg = validate_city_input("Boston")
        self.assertTrue(valid)
        self.assertIsNone(msg)

    # PASS 2
    def test_validate_city_input_empty(self):
        valid, msg = validate_city_input("   ")
        self.assertFalse(valid)
        self.assertEqual(msg, "Input cannot be empty.")

    # PASS 3
    @patch("main.requests.get")
    def test_get_coordinates_exact_match(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "name": "Boston",
                "lat": 42.3601,
                "lon": -71.0589,
                "country": "US",
                "state": "Massachusetts"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        lat, lon, country, state = get_coordinates("Boston")

        self.assertEqual(lat, 42.3601)
        self.assertEqual(lon, -71.0589)
        self.assertEqual(country, "US")
        self.assertEqual(state, "Massachusetts")

    # PASS 4
    @patch("main.requests.get")
    def test_fetch_air_quality_pass(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "list": [{"main": {"aqi": 2}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_air_quality(42.3601, -71.0589)

        self.assertEqual(result, 2)

    # FAIL 1 — intentionally failing test
    @patch("main.requests.get")
    def test_fetch_air_quality_fail(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "list": [{"main": {"aqi": 2}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_air_quality(42.3601, -71.0589)

        # This is intentionally wrong.
        # API mock returns 2, but we are expecting 5.
        self.assertEqual(result, 5)


if __name__ == "__main__":
    unittest.main()