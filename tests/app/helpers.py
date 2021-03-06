import mock
from app import create_app
from unittest import TestCase


class BaseApplicationTest(TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        self.s3 = mock.patch('app.main.views.S3').start()

    def tearDown(self):
        self.s3.stop()
