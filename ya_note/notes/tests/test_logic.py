from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.models import Note
from notes.tests.helpers import (NOTES_DELETE_URL,
                                 NOTES_SUCCESS_URL,
                                 NOTES_EDIT_URL,
                                 Helpers,
                                 NOTES_ADD_URL,
                                 SLUG)
from pytest_django.asserts import assertFormError
from pytils.translit import slugify
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(Helpers):

    def test_anonymous_user_cant_create_note(self):
        count_before = Note.objects.count()
        self.client.post(NOTES_ADD_URL, data=self.form_data)
        count_after = Note.objects.count()
        self.assertEqual(count_after, count_before)

    def test_user_can_create_note(self):
        notes_before = Note.objects.count()
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        notes_after = Note.objects.count()
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(notes_before, notes_after - 1)

    def test_empty_slug(self):
        del self.form_data['slug']
        self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        expected_slug = slugify(self.form_data['title'])
        note = Note.objects.get(slug=expected_slug)
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])

    def test_not_unique_slug(self):
        self.form_data['slug'] = SLUG
        notes_before = Note.objects.count()
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        notes_after = Note.objects.count()
        assertFormError(response,
                        'form',
                        'slug',
                        errors=(self.note.slug + WARNING))
        self.assertEqual(notes_before, notes_after)

    def test_author_can_delete_comment(self):
        notes_count_before = Note.objects.count()
        response = self.author_client.delete(NOTES_DELETE_URL)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_before - notes_count_after, 1)
        self.assertNotIn(self.note, Note.objects.all())

    def test_user_cant_delete_comment_of_another_user(self):
        notes_before = Note.objects.all()
        response = self.reader_client.delete(NOTES_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = Note.objects.all()
        self.assertQuerysetEqual(notes_after, notes_before)

    def test_author_can_edit_comment(self):
        response = self.author_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_edit_comment_of_another_user(self):
        notes_before = Note.objects.all()
        response = self.reader_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = Note.objects.all()
        self.assertQuerysetEqual(notes_after, notes_before)
