from django.test import TestCase
from rest_framework.test import APITestCase
from api.models import Notes
from api.serializers import NoteSerializer

class NoteSerializerTestCase(APITestCase):
    def setUp(self):
        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.'
        }
        self.note = Notes.objects.create(**self.note_data)
        self.serializer = NoteSerializer(instance=self.note)
