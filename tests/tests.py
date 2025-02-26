import unittest
import requests

class TestCardAPI(unittest.TestCase):

    def test_add_card(self):
        url = 'http://127.0.0.1:5000/cards'
        with open('front.jpg', 'rb') as front_file, open('back.jpg', 'rb') as back_file:
            files = {
                'imageFront': ('front.jpg', front_file, 'image/jpeg'),
                'imageBack': ('back.jpg', back_file, 'image/jpeg')
            }
            data = {
                'name': 'Sample Card'
            }

            response = requests.post(url, files=files, data=data)

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('id', response_data)
        self.assertEqual(response_data['name'], 'Sample Card')
        self.assertIn('imageFront', response_data)
        self.assertIn('imageBack', response_data)

    def test_get_cards(self):
        url = 'http://127.0.0.1:5000/cards'
        
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)

if __name__ == '__main__':
    unittest.main()