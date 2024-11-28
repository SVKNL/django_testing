from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db
LAZY_HOME = pytest.lazy_fixture('home_url')
LAZY_CLIENT = pytest.lazy_fixture('client')
LAZY_LOGIN = pytest.lazy_fixture('users_login')
LAZY_LOGOUT = pytest.lazy_fixture('users_logout')
LAZY_SIGNUP = pytest.lazy_fixture('users_signup')
LAZY_DETAIL = pytest.lazy_fixture('news_detail_url')
LAZY_EDIT = pytest.lazy_fixture('comment_edit_url')
LAZY_DELETE = pytest.lazy_fixture('comment_delete_url')
LAZY_NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
LAZY_AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
LAZY_EDIT_REDIRECT = pytest.lazy_fixture('login_edit_redirect')
LAZY_DELETE_REDIRECT = pytest.lazy_fixture('login_delete_redirect')


@pytest.mark.parametrize('url, parametrized_client, expected_status', (
    (LAZY_HOME,
     LAZY_CLIENT,
     HTTPStatus.OK),
    (LAZY_LOGIN,
     LAZY_CLIENT,
     HTTPStatus.OK),
    (LAZY_LOGOUT,
     LAZY_CLIENT,
     HTTPStatus.OK),
    (LAZY_SIGNUP,
     LAZY_CLIENT,
     HTTPStatus.OK),
    (LAZY_DETAIL,
     LAZY_CLIENT,
     HTTPStatus.OK),
    (LAZY_EDIT,
     LAZY_NOT_AUTHOR_CLIENT,
     HTTPStatus.NOT_FOUND),
    (LAZY_DELETE,
     LAZY_AUTHOR_CLIENT,
     HTTPStatus.OK),
    (LAZY_DELETE,
     LAZY_NOT_AUTHOR_CLIENT,
     HTTPStatus.NOT_FOUND),
    (LAZY_EDIT,
     LAZY_AUTHOR_CLIENT,
     HTTPStatus.OK),),
)
def test_pages_availability_for_every_user(url,
                                           parametrized_client,
                                           expected_status):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize('url, redirect', (
    (LAZY_EDIT, LAZY_EDIT_REDIRECT),
    (LAZY_DELETE, LAZY_DELETE_REDIRECT),
))
def test_del_edit_redirect(client,
                           news,
                           comment,
                           url,
                           users_login,
                           redirect):
    response = client.get(url)
    assertRedirects(response, redirect)
