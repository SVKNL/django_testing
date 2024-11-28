from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note

SLUG = 'slug'
NOTES_LIST_URL = reverse('notes:list')
NOTES_SUCCESS_URL = reverse('notes:success')
NOTES_DETAIL_URL = reverse('notes:detail', args=(SLUG,))
NOTES_EDIT_URL = reverse('notes:edit', args=(SLUG,))
NOTES_DELETE_URL = reverse('notes:delete', args=(SLUG,))
NOTES_ADD_URL = reverse('notes:add')
NOTES_HOME_URL = reverse('notes:home')
USERS_LOGIN_URL = reverse('users:login')
USERS_LOGOUT_URL = reverse('users:logout')
USERS_SIGNUP_URL = reverse('users:signup')
User = get_user_model()

class Helpers(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Название заметки',
            author=cls.author,
            text='Текст заметки',
            slug=SLUG,
        )
        cls.form_data = {'text': 'new text',
                         'title': 'new title',
                         'slug': 'new-slug'}
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.client = Client()


