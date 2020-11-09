# twitterBot
Application listenes for the Specific #tags

Once a tweet is listened bot likes the tweet and add a comment/reply 

It will also saves the tweet in the configured folder location with seperate folder (tweetid) for every tweet and writes the tweet details and the location details in a file 

Using Watchdog.Observer a handler is created when ever any new item is created it will invoke, then reads the details from the created file and then add it to MSMQ for further porcessing.
