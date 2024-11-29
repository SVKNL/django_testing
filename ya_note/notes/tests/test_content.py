from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.helpers import (NOTES_LIST_URL,
                                 NOTES_EDIT_URL,
                                 NOTES_ADD_URL,
                                 Helpers)

User = get_user_model()


class TestHomePage(Helpers):

    def test_note_listed(self):
        response = self.author_client.get(NOTES_LIST_URL)
        note = response.context['object_list'].get(id=self.note.id)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.author, note.author)

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
