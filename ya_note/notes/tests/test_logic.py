from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):

    TITLE_TEXT = 'Title'
    TEXT_TEXT = 'Text'

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        cls.user = User.objects.create(username='Author one')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.TEXT_TEXT, 'title': cls.TITLE_TEXT}

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_can_create_note_and_slug_not_none(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.TEXT_TEXT)
        self.assertEqual(note.title, self.TITLE_TEXT)
        self.assertEqual(note.author, self.user)
        self.assertIsNotNone(note.slug)

    def test_not_unique_slug(self):
        self.form_data['slug'] = 'slug'
        self.auth_client.post(self.url, data=self.form_data)
        self.auth_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)


class TestCommentEditDelete(TestCase):
    TITLE_TEXT = 'Note title'
    TEXT_TEXT = 'Note text'
    NEW_TITLE_TEXT = 'New note title'
    NEW_TEXT_TEXT = 'New note text'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Note author')
        cls.note = Note.objects.create(title=cls.TITLE_TEXT,
                                       text=cls.TEXT_TEXT,
                                       author=cls.author)
        cls.url_to_done = reverse('notes:success')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'text': cls.NEW_TEXT_TEXT,
                         'title': cls.NEW_TITLE_TEXT}

    def test_author_can_delete_comment(self):

        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.url_to_done)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_comment_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_comment(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.url_to_done)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_TEXT_TEXT)

    def test_user_cant_edit_comment_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.TEXT_TEXT)
