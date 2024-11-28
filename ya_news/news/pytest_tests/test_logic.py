from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import WARNING
from news.models import Comment
from news.pytest_tests.conftest import (COMMENT_TEXT,
                       NEW_COMMENT_TEXT,
                       FORM_DATA,
                       BAD_WORDS_FORM_DATA)

pytestmark = pytest.mark.django_db


def test_auth_user_can_create_comment(news,
                                      not_author_client,
                                      news_detail_url,
                                      comment_url):
    response = not_author_client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, comment_url)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == NEW_COMMENT_TEXT
    assert comment.author.username == 'Не автор'
    assert comment.news == news


def test_unauth_user_cant_create_comment(news, client, news_detail_url):
    client.post(news_detail_url, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_use_bad_words(not_author_client, news, news_detail_url):
    response = not_author_client.post(news_detail_url,
                                      data=BAD_WORDS_FORM_DATA)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client,
                                   comment,
                                   news,
                                   comment_delete_url,
                                   news_detail_url,
                                   comment_url):
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, comment_url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_not_author_cant_delete_comment(not_author_client,
                                        comment,
                                        news,
                                        comment_delete_url,
                                        news_detail_url):
    response = not_author_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    assert comment.text == COMMENT_TEXT
    assert comment.author.username == 'Автор'
    assert comment.news == news


def test_author_can_edit_comment(news,
                                 comment,
                                 news_detail_url,
                                 comment_edit_url,
                                 author_client,
                                 comment_url,
                                 author):
    response = author_client.post(comment_edit_url, data=FORM_DATA)
    assertRedirects(response, comment_url)
    comment = Comment.objects.get()
    assert comment.text == NEW_COMMENT_TEXT
    assert comment.author == author
    assert comment.news == news


def test_not_author_cant_edit_comment(news,
                                      comment,
                                      news_detail_url,
                                      comment_edit_url,
                                      not_author_client):
    response = not_author_client.post(comment_edit_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == COMMENT_TEXT
    assert comment.author.username == 'Автор'
    assert comment.news == news
