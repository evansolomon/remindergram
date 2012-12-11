from nose.tools import *
from remindergram import source
from remindergram import photo
from remindergram import recommendation

test_attrs = {
    'title': 'My test',
    'author': 'Evan Solomon',
    'link': 'http://evansolomon.me',
    'date': 'Tue, 11 Dec 2012 01:43:30 +0000'
}

bears = {
    'little': photo.Photo('http://placebear.com/50/100', test_attrs),
    'medium': photo.Photo('http://placebear.com/200/200', test_attrs),
    'big': photo.Photo('http://placebear.com/1000/2000', test_attrs)
}


def test_wp_plain_urls():
    assert_equals('http://evansolomon.me/feed', source.WordPress('http://evansolomon.me').url)
    assert_equals('http://evansolomon.me/tag/foo/feed', source.WordPress('http://evansolomon.me/tag/foo').url)


def test_wp_feed_urls():
    assert_equals('http://evansolomon.me/feed', source.WordPress('http://evansolomon.me/feed').url)
    assert_equals('http://evansolomon.me/tag/foo/feed', source.WordPress('http://evansolomon.me/tag/foo/feed').url)


def test_instagram_urls():
    assert_equals('http://widget.stagram.com/rss/n/foo/', source.Instagram('foo').url)


def test_wp_feed_length():
    blog = source.WordPress('http://evansolomon.me')
    assert_equals(10, len(blog.get_entries()))


def test_rss_feed_length():
    blog = source.RSS('tests/evansolomon.xml')
    assert_equals(10, len(blog.get_entries()))


def test_img_in_html():
    html = """
    <p>Here is HTML with an <img src="http://placebear.com/50/50"> image in it</p>
    </div>Here is another <img src='http://placebear.com/500/700' /></div>
    """
    found_bears = photo.find_in_html(html)
    assert_equals(2, len(found_bears))


def test_img_size():
    assert_equals((50, 100), bears['little'].size)


def test_img_validate():
    assert_equals(False, bears['little'].validate())
    assert_equals(True, bears['big'].validate())


def test_img_validate_custom_size():
    assert_equals(False, bears['little'].validate(200))
    assert_equals(True, bears['medium'].validate(200))
    assert_equals(True, bears['big'].validate(200))


def test_recommendation_unlimited():
    blog = source.RSS('tests/evansolomon.xml')
    recs = recommendation.Recommendation(blog.photos, {'validate_days': -1})
    assert_equals(len(blog.get_entries()), len(recs.recommendations))


def test_recommendation_limited():
    blog = source.RSS('tests/evansolomon.xml')
    recs = recommendation.Recommendation(blog.photos, {'validate_days': 1})
    assert_equals(0, len(recs.recommendations))


def test_recommendation_instagram():
    chexstagram = source.Instagram('chexee')
    recs = recommendation.Recommendation(chexstagram.photos, {'validate_days': -1, 'validate_size': 300})
    assert_equals(len(chexstagram.get_entries()), len(recs.recommendations))
