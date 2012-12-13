from nose.tools import *
from remindergram import source
from remindergram import photo
from remindergram import recommendation

bear_photo_attrs = {
    'title': 'My test',
    'author': 'Evan Solomon',
    'link': 'http://evansolomon.me',
    'timestamp': 1355219010
}

bears = {
    'little': photo.Photo('http://placebear.com/50/100', bear_photo_attrs),
    'medium': photo.Photo('http://placebear.com/200/200', bear_photo_attrs),
    'big': photo.Photo('http://placebear.com/1000/2000', bear_photo_attrs)
}

chexstagram = source.Instagram('chexee')

wp_plain = {
    'root': source.WordPress('http://evansolomon.me'),
    'tag': source.WordPress('http://evansolomon.me/tag/foo')
}

wp_feed = {
    'root': source.WordPress('http://evansolomon.me/feed'),
    'tag': source.WordPress('http://evansolomon.me/tag/foo/feed')
}

rss = source.RSS('tests/evansolomon.xml')


def test_wp_plain_urls():
    assert_equals('http://evansolomon.me/feed', wp_plain.get('root').url)
    assert_equals('http://evansolomon.me/tag/foo/feed', wp_plain.get('tag').url)


def test_wp_feed_urls():
    assert_equals('http://evansolomon.me/feed', wp_feed.get('root').url)
    assert_equals('http://evansolomon.me/tag/foo/feed', wp_feed.get('tag').url)


def test_instagram_urls():
    assert_equals('http://widget.stagram.com/rss/n/chexee/', chexstagram.url)


def test_wp_feed_length():
    blog = wp_plain.get('root')
    assert_equals(10, len(blog.get_entries()))


def test_rss_feed_length():
    assert_equals(10, len(rss.get_entries()))


def test_img_in_html():
    html = """
    <p>Here is HTML with an <img src="http://placebear.com/50/50"> image in it</p>
    <div>Here is another <img src='http://placebear.com/500/700' /></div>
    <span>Here is another <img alt="bear!" src='http://placebear.com/5/5' /></span>
    """
    found_bears = photo.find_in_html(html)
    assert_equals(3, len(found_bears))


def test_img_size():
    assert_equals((50, 100), bears['little'].size)
    assert_equals((200, 200), bears['medium'].size)
    assert_equals((1000, 2000), bears['big'].size)


def test_img_validate():
    assert_equals(False, bears['little'].validate())
    assert_equals(True, bears['big'].validate())


def test_img_validate_custom_size():
    assert_equals(False, bears['little'].validate(200))
    assert_equals(True, bears['medium'].validate(200))
    assert_equals(True, bears['big'].validate(200))


def test_recommendation_unlimited():
    recs = recommendation.Recommendation(rss.photos, {'days': 0})
    assert_equals(len(rss.get_entries()), len(recs.get()))


def test_recommendation_limited():
    recs = recommendation.Recommendation(rss.photos, {'days': 1})
    assert_equals(0, len(recs.get()))


def test_recommendation_instagram():
    recs = recommendation.Recommendation(chexstagram.photos, {'days': 0, 'size': 500})
    assert_equals(len(chexstagram.get_entries()), len(recs.get()))
