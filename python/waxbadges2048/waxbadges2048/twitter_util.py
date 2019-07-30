import twitter

from django.conf import settings


def get_api():
    return twitter.Api( consumer_key=settings.TWITTER_INTERNAL_CONSUMER_KEY,
                        consumer_secret=settings.TWITTER_INTERNAL_CONSUMER_SECRET,
                        access_token_key=settings.TWITTER_INTERNAL_ACCESS_TOKEN,
                        access_token_secret=settings.TWITTER_INTERNAL_ACCESS_SECRET)


def get_user(username):
    return get_api().GetUser(screen_name=username)


def get_avatarurl(username):
    twitter_api = get_api()
    twitter_user = twitter_api.GetUser(screen_name=username)
    avatarurl = twitter_user.profile_image_url_https

    return avatarurl.replace('_normal', '')


def dm_user(username, msg):
    twitter_api = get_api()
    twitter_api.PostDirectMessage(text=msg, screen_name=username)
