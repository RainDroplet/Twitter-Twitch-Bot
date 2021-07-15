# Twitter Bot
 Personal project used to learn the Twitter & Twitch API

 This version of the bot is intentinally not going to have parts that will allow it to run. 

Have access to twitch and twitter APIs

Objective:
    When Poki tweets [cannot be retweets], the bot will like, retweet and comment.
    When Poki is online on twitch, the bot will tweet out that Poki is streaming.

To Do:
    - Import twitter api (done)
        Tweepy
    - Import twitch api (done)
        twitchAPI
    - Create stream that watching Poki's twitter (kinda)
        > created a tweet puller that will check the recent tweets and compare if they have been tweeted before
    - Create a general API config and boot up (done)
    - Create a unique comment system that looks up keyphrases via Poki's Twitter (basic but done)
    - Create a checker to see if Poki is streaming (done)
    - Automatic generic tweets at set different times of the day (done)


Auto tweeting
    Based off of current computer time, it will automatically tweet about something
        ie. 'Good morning fellow human simps!'

Liking and retweeting process
    Bot Pulls from Poki's Twitter's recent 30 tweets
        -> Check if tweet is a retweet
            if retweet then ignore
            if tweet
                -> retweets onto bot page
                -> likes tweet
                -> unique* comment
                *unique comments requires me to pull and compare the tweet content for key words to determine what kind
                response is needed for that tweet
                    ex.
                    Poki tweet below ▼
                    ---------------------------------------------------------------------------------------------------
                    if you've ever wanted a behind-the-scenes look at the business side of streaming,
                    then check out my collab with graham stephan!

                    link below~
                    https://youtu.be/wvl05CQKkY0
                    ---------------------------------------------------------------------------------------------------

                    keyword for video tweets -> 'youtu.be'

                    unique response -> 'Bless up, our queen has graced us with a video.
                                        This was made from the simp bot gang.'


Tweeting about Poki's Stream being online
    Bot checks if Poki's Stream status
        -> Check if she is online or offline
            if offline do nothing
            if online tweets
                -> Tweets onto page saying 'Our queen is streaming. Go watch fellow simps!
                                            https://www.twitch.tv/pokimane'

Layout
Poki Simp Bot/
│
├── config.py
├── PokiTwitterTwitch.py
│
├── Bot_Info.txt
└── Documentation.txt
│
└── runtime_info.log

God bless Evan for all your help