from rest_framework.test import APIClient
from dresses.models import Dress, Brand
from dresses.serializers import DressSerializer, BrandSerializer
import unittest
from django.urls import reverse
from unittest.mock import patch

from dresses.views import show_average_pieces

class TestFilterBrandsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('dresses.views.Brand.objects.all')
    def test_filter_brands(self, mock_all):
        nr_models=2
        response = self.client.get(f'/brands/filter/{nr_models}')
        self.assertEqual(response.status_code, 200)

        expected_data = BrandSerializer(Brand.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)



class ShowAveragePiecesTestCase(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('dresses.models.ShowEvent')
    def test_show_average_pieces(self,mock):
        url = reverse(show_average_pieces)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expected_data= "RedCarpetPresentation ID: 9, Average Pieces: 30.4                                        RedCarpetPresentation ID: 1, Average Pieces: 30.0                                        RedCarpetPresentation ID: 5, Average Pieces: 30.0                                        RedCarpetPresentation ID: 7, Average Pieces: 11.0                                        RedCarpetPresentation ID: 6, Average Pieces: 10.0                                        RedCarpetPresentation ID: 2, Average Pieces: 6.0                                        RedCarpetPresentation ID: 10, Average Pieces: 1.0                                        "

        self.assertEqual(response.data, expected_data)


if __name__ == '_main_':
        unittest.main()