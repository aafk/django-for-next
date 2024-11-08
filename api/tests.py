from django.test import TestCase
from .models import *

# Create your tests here.
class AccountLevelTest(TestCase):
    def setUp(self):
        AccountLevel.objects.create(name="lion", parent=0)

    def getall(self):
        level1 = AccountLevel.objects.filter(level=1)
        print(level1)