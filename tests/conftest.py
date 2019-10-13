"""Helpers and fixtures for pytest."""
import re
from unittest import mock

from aioresponses import aioresponses
from pytest import fixture

from group_songlink_bot.bot import SonglinkBot
from group_songlink_bot.config import TestConfig

TEST_RESPONSE = {
    'entitiesByUniqueId': {
        'DEEZER_SONG::D1': {
            'id': 'D1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'deezer',
        },
        'ITUNES_SONG::IT1': {
            'id': 'IT1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'itunes',
        },
        'SPOTIFY_SONG::S1': {
            'id': 'S1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'spotify',
        },
        'GOOGLE_SONG::G1': {
            'id': 'G1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'google',
        },
        'AMAZON_SONG::A1': {
            'id': 'A1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'amazon',
        },
        'TIDAL_SONG::T1': {
            'id': 'T1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'tidal',
        },
        'NAPSTER_SONG::N1': {
            'id': 'N1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'napster',
        },
        'YANDEX_SONG::Y1': {
            'id': 'Y1',
            'title': 'Test Title',
            'artistName': 'Test Artist',
            'apiProvider': 'yandex',
        },
    },
    'linksByPlatform': {
        'deezer': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'DEEZER_SONG::D1',
        },
        'appleMusic': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'ITUNES_SONG::IT1',
        },
        'spotify': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'SPOTIFY_SONG::S1',
        },
        'youtube': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'YOUTUBE_VIDEO::Y1',
        },
        'youtubeMusic': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'YOUTUBE_VIDEO::YM1',
        },
        'google': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'GOOGLE_SONG::G1',
        },
        'amazonMusic': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'AMAZON_SONG::A1',
        },
        'tidal': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'TIDAL_SONG::T1',
        },
        'napster': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'NAPSTER_SONG::N1',
        },
        'yandex': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'YANDEX_SONG::Y1',
        },
        'itunes': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'ITUNES_SONG::IT1',
        },
        'googleStore': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'GOOGLE_SONG::G1',
        },
        'amazonStore': {
            'url': 'https://www.test.com/test',
            'entityUniqueId': 'AMAZON_SONG::A1',
        },
    },
}


@fixture
def test_config():
    """Test config fixture."""
    config = TestConfig.load_config()
    return config


@fixture
async def bot(test_config):
    """Bot fixture."""

    def mock_check_token(token):
        return True

    with mock.patch('aiogram.bot.api.check_token', mock_check_token):
        bot = SonglinkBot(config=test_config)
        yield bot
    await bot.stop()


@fixture
async def songlink_api(test_config):
    """Songlink API mock."""
    pattern = re.compile(rf'^{re.escape(test_config.SONGLINK_API_URL)}.*$')
    with aioresponses() as m:
        m.get(pattern, status=200, payload=TEST_RESPONSE)
        yield m
