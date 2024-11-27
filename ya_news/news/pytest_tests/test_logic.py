from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment



@pytest.mark.django_db
def test_auth_user_can_create_comment(news, not_author_client, form_data):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = not_author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']

@pytest.mark.django_db
def test_unauth_user_cant_create_comment(news, client, form_data):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0

@pytest.mark.django_db
def test_user_cant_use_bad_words(not_author_client, form_data, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = not_author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0

@pytest.mark.django_db
def test_author_can_delete_comment(author_client,
                                   comment,
                                   news,
                                   comment_delete_url,
                                   news_detail_url):
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, f'{news_detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_not_author_can_delete_comment(not_author_client,
                                   comment,
                                   news,
                                   comment_delete_url,
                                   news_detail_url):
    response = not_author_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1

@pytest.mark.django_db
def test_author_can_edit_comment(news,
                                 comment,
                                 news_detail_url,
                                 comment_edit_url,
                                 form_data,
                                 author_client):
    response = author_client.post(comment_edit_url, data=form_data)
    assertRedirects(response, f'{news_detail_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']

@pytest.mark.django_db
def test_author_can_edit_comment(news,
                                 comment,
                                 news_detail_url,
                                 comment_edit_url,
                                 form_data,
                                 not_author_client):
    response = not_author_client.post(comment_edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Comment text'

