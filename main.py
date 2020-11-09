import json
import os
import watchdog
import tweepy
from time import sleep

TWEET_DIR_PATH = 'D:\\Projects\\Personal\\twitter_bot\\tweets'
consumer_key = str(os.environ.get("CONSUMER_KEY"))
consumer_secret = str(os.environ.get("CONSUMER_SECRET"))
access_token = str(os.environ.get("ACCESS_TOKEN"))
access_token_secret = str(os.environ.get("ACCESS_TOKEN_SECRET"))

'''
CreatedMyStreamListener to listen for any new tweets tweeted with specific #tag
on_status(): Callback received once a tweet is tweeted with the corresponding #tag
'''
class MyStreamListener(tweepy.StreamListener):
  def __init__(self, api):
    self.api = api
    self.me = api.me()

  def on_status(self, tweet):
    print(f"{tweet.user.name}:{tweet.text}")
    print(tweet)
    save_tweet(tweet=tweet,api=self.api)
    geo_location = get_location(tweet)

  def on_error(self, status):
    print("Error detected")


'''
This method returns the location of the tweet if location is mentioned
Retuns
      Null/Empty: If no location is tagged to the tweet
      Location Details: If a location is tagged to the tweet
'''
def get_location(tweet):
    location = ''
    print(tweet._json['place'])
    return location


'''
Method to fetch the authorization to access the twitter api
'''


def get_authorization():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

'''
Method used to save the tweet details in a file with the tweet Id 
It also likes the tweet 
'''
def save_tweet(tweet,api):
    if(os.path.exists(TWEET_DIR_PATH) == False):
        os.mkdir(TWEET_DIR_PATH)
    else:
        tweet_details = json.dumps(tweet._json)
        tweet_json = json.loads(tweet_details)
        tweet_id = tweet_json['id']
        tweet_text_dir = ''
        if(os.path.exists(TWEET_DIR_PATH + '\\' + str(tweet_id)) == False):
            tweet_text_dir = TWEET_DIR_PATH + '\\' + str(tweet_id)
            os.mkdir(tweet_text_dir)
        
        fileName = tweet_text_dir + '\\' +str(tweet_id) + '.txt'
        print(fileName)
        file_ptr = open(fileName, "w+")
        file_ptr.writelines('tweet_text:'+tweet_json['text'])
        file_ptr.write("\n")
        if(tweet_json['place']):
          file_ptr.writelines('place_type:'+ tweet_json['place']['place_type'])
          file_ptr.write("\n")
          file_ptr.writelines('place_fullname:'+ tweet_json['place']['full_name'])
          file_ptr.write("\n")
          file_ptr.writelines('bounding_box_type:' + tweet_json['place']['bounding_box']['type'])
          file_ptr.write("\n")
          file_ptr.writelines('bounding_box_coord:' + str(tweet_json['place']['bounding_box']['coordinates']))
          file_ptr.write("\n")
        
        file_ptr.close()
        api.create_favorite(tweet_id)
        reply_tweet(api=api,tweet=tweet,reply_messasge="Replied")
        

def reply_tweet(api, tweet, reply_messasge):
  api.update_status(status=reply_messasge,
                    in_reply_to_status_id=tweet._json['id'], auto_populate_reply_metadata=True)



'''
Returns the user details about the give User
userId: screen name or the id of the user
'''
def get_userInfo(api,userId):
  user_info = api.get_user(userId)
  return user_info


def tweetSerach(api,searchString):
  tweetsSearchInfo = tweepy.Cursor(api.search, q=searchString).items(10)
  for tweet in tweetsSearchInfo:
    print(f"{tweet}")



def get_tweet_location():
    location=''
    return location


api = get_authorization()
#input('Please enter the User Name you want to search')
userId = 'pavankuk'
user_info = get_userInfo(api,userId)
print(user_info)

#Creating Stream
customStreamListener = MyStreamListener(api)
customStream = tweepy.Stream(auth=api.auth,listener=customStreamListener)
customStream.filter(track=['#abc1234abc12351234567890'],languages=['en'])


