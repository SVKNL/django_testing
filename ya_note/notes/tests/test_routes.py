from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.helpers import (NOTES_DELETE_URL,
                                 NOTES_SUCCESS_URL,
                                 NOTES_EDIT_URL,
                                 Helpers,
                                 NOTES_ADD_URL,
                                 NOTES_DETAIL_URL,
                                 NOTES_LIST_URL,
                                 USERS_LOGIN_URL,
                                 NOTES_HOME_URL,
                                 USERS_LOGOUT_URL,
                                 USERS_SIGNUP_URL,
                                 LOGIN_REDIRECT_EDIT_URL,
                                 LOGIN_REDIRECT_DELETE_URL,
                                 LOGIN_REDIRECT_LIST_URL,
                                 LOGIN_REDIRECT_SUCCESS_URL,
                                 LOGIN_REDIRECT_DETAIL_URL)

User = get_user_model()


class TestRoutes(Helpers):

    def test_availability_for_note_detail_edit_and_delete(self):
        cases = [[NOTES_HOME_URL, self.client, HTTPStatus.OK],
                 [USERS_LOGIN_URL, self.client, HTTPStatus.OK],
                 [USERS_LOGOUT_URL, self.client, HTTPStatus.OK],
                 [USERS_SIGNUP_URL, self.client, HTTPStatus.OK],
                 [NOTES_EDIT_URL, self.author_client, HTTPStatus.OK],
                 [NOTES_DELETE_URL, self.author_client, HTTPStatus.OK],
                 [NOTES_ADD_URL, self.author_client, HTTPStatus.OK],
                 [NOTES_EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND],
                 [NOTES_DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND],
                 [NOTES_ADD_URL, self.reader_client, HTTPStatus.OK],
                 [NOTES_LIST_URL, self.client, HTTPStatus.FOUND],
                 [NOTES_EDIT_URL, self.client, HTTPStatus.FOUND],
                 [NOTES_DELETE_URL, self.client, HTTPStatus.FOUND],
                 [NOTES_DETAIL_URL, self.client, HTTPStatus.FOUND],
                 [NOTES_SUCCESS_URL, self.client, HTTPStatus.FOUND], ]
        for url, client, status in cases:
            with self.subTest(name=url, client=client, status=status):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        cases = [[NOTES_EDIT_URL, LOGIN_REDIRECT_EDIT_URL],
                  [NOTES_DELETE_URL, LOGIN_REDIRECT_DELETE_URL],
                  [NOTES_DETAIL_URL, LOGIN_REDIRECT_DETAIL_URL],
                  [NOTES_LIST_URL, LOGIN_REDIRECT_LIST_URL],
                  [NOTES_SUCCESS_URL, LOGIN_REDIRECT_SUCCESS_URL]]
        for url, redirect in cases:
            with self.subTest(name=url, redirect=redirect):
                response = self.client.get(url)
                self.assertRedirects(response, redirect)
