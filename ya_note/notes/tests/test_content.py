from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from .helpers import NOTES_LIST_URL, NOTES_EDIT_URL, NOTES_ADD_URL, Helpers, SLUG

User = get_user_model()


class TestHomePage(Helpers):

    def test_note_listed(self):
        response = self.author_client.get(NOTES_LIST_URL)
        note = response.context['object_list'].get()
        self.assertEqual(self.note, note)
        self.assertEqual(note.title, 'Название заметки')
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, SLUG)
        self.assertEqual(note.text, 'Текст заметки')

    def test_note_for_author_only(self):
        response = self.reader_client.get(NOTES_LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_authorized_client_has_form(self):
        for url in (NOTES_EDIT_URL, NOTES_ADD_URL):
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
