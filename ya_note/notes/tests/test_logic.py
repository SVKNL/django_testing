from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.models import Note
from notes.tests.helpers import (NOTES_DELETE_URL,
                      NOTES_SUCCESS_URL,
                      NOTES_EDIT_URL,
                      Helpers,
                      NOTES_ADD_URL,
                      SLUG)

User = get_user_model()


class TestNoteCreation(Helpers):

    def test_anonymous_user_cant_create_note(self):
        self.client.post(NOTES_ADD_URL, data=self.form_data)
        slugs = list(Note.objects.values_list('slug', flat=True))
        self.assertNotIn('new-slug', slugs)

    def test_user_can_create_note(self):
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note = Note.objects.get(slug='new-slug')
        self.assertEqual(note.text, 'new text')
        self.assertEqual(note.title, 'new title')
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, 'new-slug')

    def test_empty_slug(self):
        del self.form_data['slug']
        self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        note = Note.objects.get(text='new text')
        self.assertIsNotNone(note.slug)

    def test_not_unique_slug(self):
        self.form_data['slug'] = SLUG
        self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        notes_count = Note.objects.filter(slug=SLUG).count()
        self.assertLess(notes_count, 2)


class TestCommentEditDelete(Helpers):

    def test_author_can_delete_comment(self):
        notes_count_before = Note.objects.count()
        response = self.author_client.delete(NOTES_DELETE_URL)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_before - notes_count_after, 1)

    def test_user_cant_delete_comment_of_another_user(self):
        response = self.reader_client.delete(NOTES_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(slug=SLUG)
        self.assertEqual(note.text, 'Текст заметки')
        self.assertEqual(note.title, 'Название заметки')
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, SLUG)

    def test_author_can_edit_comment(self):
        response = self.author_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note = Note.objects.get(slug='new-slug')
        self.assertEqual(note.text, 'new text')
        self.assertEqual(note.title, 'new title')
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, 'new-slug')

    def test_user_cant_edit_comment_of_another_user(self):
        response = self.reader_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(slug=SLUG)
        self.assertEqual(note.text, 'Текст заметки')
        self.assertEqual(note.title, 'Название заметки')
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, SLUG)
