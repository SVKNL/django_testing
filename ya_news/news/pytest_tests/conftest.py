from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.test.client import Client

from news.models import News, Comment
from news.forms import BAD_WORDS

COMMENT_TEXT = 'Comment text'
NEW_COMMENT_TEXT = 'New comment text'
BAD_WORDS_COMMENT = f'bla-bla {BAD_WORDS[0]}'
FORM_DATA = {'text': NEW_COMMENT_TEXT}
BAD_WORDS_FORM_DATA = {'text': BAD_WORDS_COMMENT}


@pytest.fixture()
def client():
    client = Client()
    return client


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',

    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        text=COMMENT_TEXT,
        author=author,
        news=news,
    )
    return comment


@pytest.fixture
def multiple_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def multiple_comments(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', kwargs={'pk': news.id})


@pytest.fixture
def comment_delete_url(news, comment):
    return reverse('news:delete', kwargs={'pk': comment.id})


@pytest.fixture
def comment_edit_url(news, comment):
    return reverse('news:edit', kwargs={'pk': comment.id})


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def comment_url(news_detail_url):
    return f'{news_detail_url}#comments'


@pytest.fixture
def users_login():
    return reverse('users:login')


@pytest.fixture
def users_logout():
    return reverse('users:logout')


@pytest.fixture
def users_signup():
    return reverse('users:signup')
