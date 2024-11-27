import pytest
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_pagination_om_main(client, multiple_news_creation):
    url = reverse('news:home')
    response = client.get(url)
    news_on_main_number = response.context['object_list'].count()
    assert news_on_main_number == 10


@pytest.mark.django_db
def test_sorted_on_main(client, multiple_news_creation):
    url = reverse('news:home')
    response = client.get(url)
    news_on_main = response.context['object_list']
    all_dates = [news.date for news in news_on_main]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


@pytest.mark.django_db
def test_comments_sorted(client, multiple_comments_creation, news):
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    # Собираем временные метки всех комментариев.
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_comment_creation_available_for_anon_user(news, client):
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_comment_creation_available_for_auth_user(news, not_author_client):
    url = reverse('news:detail', args=[news.id])
    response = not_author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)



