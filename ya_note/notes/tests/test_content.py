from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestHomePage(TestCase):
    LISTING_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author_one = User.objects.create(username='Автор_one')
        cls.author_two = User.objects.create(username='Author two')
        cls.note_one = Note.objects.create(title='Test note one',
                                           text='Test text one',
                                           author=cls.author_one)
        cls.note_two = Note.objects.create(title='Test note two',
                                           text='Test text two',
                                           author=cls.author_two)

    def test_note_listed(self):
        self.client.force_login(self.author_one)
        response = self.client.get(self.LISTING_URL)
        note = response.context['object_list']
        self.assertEqual(note[0], self.note_one)

    def test_note_for_author_only(self):
        self.client.force_login(self.author_one)
        response = self.client.get(self.LISTING_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note_two, notes)

    def test_authorized_client_has_form(self):
        for name, args in (('notes:edit', (self.note_one.slug,)),
                           ('notes:add', None)):
            with self.subTest(name=name):
                self.client.force_login(self.author_one)
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
