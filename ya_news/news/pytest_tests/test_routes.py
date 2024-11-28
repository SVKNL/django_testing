from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('url, parametrized_client, expected_status', (
    (pytest.lazy_fixture('home_url'),
     pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('users_login'),
     pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('users_logout'),
     pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('users_signup'),
     pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('news_detail_url'),
     pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('comment_edit_url'),
     pytest.lazy_fixture('not_author_client'),
     HTTPStatus.NOT_FOUND),
    (pytest.lazy_fixture('comment_delete_url'),
     pytest.lazy_fixture('author_client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('comment_delete_url'),
     pytest.lazy_fixture('not_author_client'),
     HTTPStatus.NOT_FOUND),
    (pytest.lazy_fixture('comment_edit_url'),
     pytest.lazy_fixture('author_client'),
     HTTPStatus.OK),),
    )
def test_pages_availability_for_every_user(url,
                                           parametrized_client,
                                           expected_status):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('comment_edit_url'),
     pytest.lazy_fixture('comment_delete_url')),
)
def test_del_edit_redirect(client, news, comment, url, users_login):
    expected_url = f'{users_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
