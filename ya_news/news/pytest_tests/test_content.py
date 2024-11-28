import pytest
pytestmark = pytest.mark.django_db


def test_pagination_om_main(client, multiple_news, home_url):
    response = client.get(home_url)
    news_on_main_number = response.context['object_list'].count()
    assert news_on_main_number == 10


def test_sorted_on_main(client, multiple_news, home_url):
    response = client.get(home_url)
    news_on_main = response.context['object_list']
    all_dates = [news.date for news in news_on_main]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


def test_comments_sorted(client, multiple_comments, news, news_detail_url):
    response = client.get(news_detail_url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_comment_creation_available_for_anon_user(news,
                                                  client,
                                                  news_detail_url):
    response = client.get(news_detail_url)
    assert 'form' not in response.context


def test_comment_creation_available_for_auth_user(news,
                                                  not_author_client,
                                                  news_detail_url):
    response = not_author_client.get(news_detail_url)
    assert 'form' in response.context
    form_object = response.context.get('form')
    assert form_object is not None
