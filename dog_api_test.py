import unittest
from unittest.mock import patch
import builtins
import dog_api  # This is your main student file (rename if needed)

class TestDogAPIBrowser(unittest.TestCase):

    @patch('dog_api.requests.get')
    def test_get_all_breeds_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "message": {
                "bulldog": ["boston", "english", "french"],
                "retriever": ["golden"]
            },
            "status": "success"
        }

        breeds = dog_api.get_all_breeds()
        self.assertIn("bulldog", breeds)
        self.assertIn("retriever", breeds)
        self.assertEqual(len(breeds["bulldog"]), 3)

    @patch('dog_api.requests.get')
    def test_get_all_breeds_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")
        with self.assertRaises(Exception):
            dog_api.get_all_breeds()


    @patch('dog_api.requests.get')
    def test_get_random_image_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "message": "https://images.dog.ceo/breeds/retriever-golden/n02099601_123.jpg",
            "status": "success"
        }

        url = dog_api.get_random_image("retriever")
        self.assertTrue(url.startswith("https://images.dog.ceo/"))

    @patch('dog_api.requests.get')
    def test_get_random_image_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        with self.assertRaises(Exception):
            dog_api.get_random_image("invalidbreed")

    @patch('dog_api.requests.get')
    def test_get_random_sub_breed_image_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "message": "https://images.dog.ceo/breeds/bulldog-english/n02096585_345.jpg",
            "status": "success"
        }

        url = dog_api.get_random_sub_breed_image("bulldog", "english")
        self.assertTrue("bulldog-english" in url)

    @patch('dog_api.requests.get')
    def test_get_random_sub_breed_image_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        with self.assertRaises(Exception):
            dog_api.get_random_sub_breed_image("bulldog", "notreal")

    def test_show_breeds_formatting(self):
        breeds_dict = {
            "bulldog": ["english", "french"],
            "retriever": ["golden"],
            "poodle": [],
            "beagle": [],
            "husky": [],
            "shiba": [],
        }

        with patch("builtins.print") as mock_print:
            dog_api.show_breeds(breeds_dict)
            # Should print all breeds, 5 per line
            flat_breeds = sorted(breeds_dict.keys())
            self.assertTrue(any(flat_breeds[0] in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any(flat_breeds[-1] in call[0][0] for call in mock_print.call_args_list))

    @patch("builtins.input", side_effect=["4"])
    def test_exit_main_loop(self, mock_input):
        with patch("builtins.print") as mock_print:
            dog_api.main()
            self.assertTrue(any("Goodbye" in call[0][0] for call in mock_print.call_args_list))

