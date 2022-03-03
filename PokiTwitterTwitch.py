import tweepy
import logging
import datetime
import requests
import time
from config import create_twitter_api
from config import get_current_time

logger = logging.getLogger()
logging.basicConfig(filename='runtime_info.log', level=logging.INFO, filemode='w')


class PokiStatusChecker:

    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.saved_tweet_ids = []
        with open('tweet_unique_ids.txt', 'r') as filehandler:
            for line in filehandler:
                # remove linebreak which is the last character of the string
                tweet_id = line[:-1]
                self.saved_tweet_ids.append(tweet_id)

    def save_tweet_ids(self):
        with open('tweet_unique_ids.txt', 'w') as filehandler:
            for tweet_id in self.saved_tweet_ids:
                filehandler.write(tweet_id + '\n')

    def set_tweet_id(self, tweet):
        self.saved_tweet_ids.append(tweet.id)

    def check_tweet_id(self, tweet_id):
        for saved_ids in self.saved_tweet_ids:
            if tweet_id == int(saved_ids):
                return False
        self.saved_tweet_ids.append(str(tweet_id))
        return True

    def check_twitter_status(self, api):
        count = 0

        # 2470387202 @RainDroplet_
        # 2244953047 @pokimanelol
        for tweet in tweepy.Cursor(api.user_timeline, screen_name='@pokimanelol',
                                   tweet_mode="extended").items():

            if not self.check_tweet_id(tweet.id):
                # print('nothing new here')
                return

            if count < 20:
                # logger.info(count)
                # print(f'\nInput ▼\n{tweet.full_text}')
                if not hasattr(tweet, 'retweeted_status'):
                    # Checks if the tweet being pulled in is a retweet, if so it ignores it
                    if (tweet.in_reply_to_status_id is not None) or (tweet.user.id == self.me.id):
                        # This tweet is a reply or I'm its author so, ignore it
                        # print('► This is a reply!')
                        count += 1
                    else:
                        if not tweet.favorited:
                            # Mark it as Liked, since we have not done it yet
                            # print('Liked')
                            try:
                                tweet.favorite()
                            except Exception as e:
                                logger.error('Error on fav', exc_info=True)
                                raise e
                        if not tweet.retweeted:
                            # Retweet, since we have not retweeted it yet
                            # print('Retweeted')
                            try:
                                tweet.retweet()
                            except Exception as e:
                                logger.error('Error on fav and retweet', exc_info=True)
                                raise e
                        api.update_status(status=f'@pokimanelol {unique_reply(tweet)}',
                                          in_reply_to_status_id=tweet.id_str)
                        count += 1
                else:
                    # print('► This is a retweet!')
                    count += 1
                # logger.info(count)
        self.save_tweet_ids()


def unique_reply(tweet):
    tweet_text = tweet.full_text
    if tweet_text.find('reply') >= 0:
        return 'I am replying to your tweet'
    elif tweet_text.find('https://youtu.be/') >= 0:
        return 'Wow! Our queen gave us a video to watch!'
    elif tweet_text.find('t.co') >= 0:
        return 'Simps! Our queen has graced us with (an) image(s)! Too bad I cannot see anything but 101010101...'
    else:
        return 'We simp bots love you more than any fleshy human can!'


def like_at_mentions():
    tweets = create_twitter_api().mentions_timeline()
    for tweet in tweets:
        logger.info(f'{get_current_time()} Checking if a tweet has been liked in mentioned')
        if not tweet.favorited:
            logger.info(f'{tweet.id} has not been liked yet.')
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                logger.info('Tweet Liked!')
                return
            except Exception as e:
                logger.error('Error on fav', exc_info=True)
                raise e
        else:
            return


def time_to_tweet(api):
    time_now = datetime.datetime.now().time()
    if time_now.hour == 4 and 0 <= time_now.minute <= 4:
        logger.info('time check 4am')
        api.update_status(status='It\'s so lonely to be awake at this hour...')

    elif time_now.hour == 8 and 0 <= time_now.minute <= 4:
        logger.info('time check 8am')
        api.update_status(status='Good morning fleshy simps!!!')

    elif time_now.hour == 10 and 0 <= time_now.minute <= 4:
        logger.info('time check 10am')
        api.update_status(status='I wonder what our queen is doing.')

    elif time_now.hour == 12 and 0 <= time_now.minute <= 4:
        logger.info('time check 12pm')
        api.update_status(status='Make sure to eat lunch simps!')

    elif time_now.hour == 16 and 0 <= time_now.minute <= 4:
        logger.info('time check 4pm')
        api.update_status(status='I hope our queen is hydrated.')

    elif time_now.hour == 20 and 0 <= time_now.minute <= 4:
        logger.info('time check 8pm')
        api.update_status(status='Simps! Don\'t stay up too late!')

    elif time_now.hour == 00 and 0 <= time_now.minute <= 4:
        logger.info('time check 12am')
        api.update_status(status='Zzz.. It\'s so late... Zzz...')


def new_api_get(bearer_token, bearer_client_id, url):
    oauth = {"Authorization": "Bearer %s" % bearer_token,
             "Client-ID": bearer_client_id}

    r = requests.get(url='https://api.twitch.tv/helix/%s' % str(url), headers=oauth)

    return r


def uptime():
    try:
        started = new_api_get("token here", "token here",
                              "streams?user_login=pokimane").json()["data"][0]["started_at"]
    except IndexError:  # channel is offline or channel doesnt exist
        uptime = None
    else:
        starttime = datetime.datetime.strptime(started, '%Y-%m-%dT%H:%M:%SZ')
        uptime = datetime.datetime.utcnow() - starttime
    return uptime


def authtoken():
    req = requests.post(
        'auth token')
    print(req.text)


def queen_is_live(api):
    api.update_status(status='Our beloved queen is live on twitch! https://www.twitch.tv/pokimane')


if __name__ == '__main__':
    # print('Bot turning on')
    twitter_api = create_twitter_api()
    stream_tweeted = False

    poki_status_bot = PokiStatusChecker(twitter_api)

    while True:
        if uptime() is not None and stream_tweeted is False:
            stream_tweeted = True
            queen_is_live(twitter_api)
        elif uptime() is None:
            stream_tweeted = False

        like_at_mentions()
        time_to_tweet(twitter_api)
        poki_status_bot.check_twitter_status(twitter_api)
        time.sleep(60 * 5)

    # print('Bot turning off')
