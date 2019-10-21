
#notes:
#1)Add exception handling everywhere
#2)Keep applying things that you learn about tweepy and textblob

import time
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import sys 

consumer_key="Ee0lw604kCAuzTbFp3pcn5lck"
consumer_secret="uuedTNbrDhmhsI8QBeOeCcEaOxtoe4nXDPDcRd8XkLF67yzjQ1"

access_token="857652506079490048-pPDneGr61On9KS4KQ5yWG4wHZCvvdMz"
access_token_secret="kZEayyj3UM56Lf9xkk10yNgr8wCod6JXgnu0BueKcN5f7"


auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api=tweepy.API(auth)
search_string="Demons"
def pen(search_string):
    pass
def ears():
     tweets=[]
     sentiment=[]
     subjectivity=[]
     print("What keyword do you want the Boy of Silence to look for?")
     search_string=input('>')
     public_tweets=api.search(search_string)
     count=0
     labels=["Tweet","Sentiment","Subjectivity"]
     for tweet in public_tweets:
         
         tweets.append(tweet.text)
         print("*"*19)
         print("Index:",count)
         print(tweets[count])
         analysis=TextBlob(tweet.text)
         sentiment.append(analysis.sentiment[0])
         subjectivity.append(analysis.sentiment[1])
         print("Sentiment",sentiment[count])
         print("Subjectivity",subjectivity[count])
         count+=1
         print("*"*19)
     #print(tweets)
     #print(sentiment)
     #print(subjectivity)
     dataset=[]
     for i in range(0,len(tweets)):
         dataset.append([tweets[i],sentiment[i],subjectivity[i]])
     #print(dataset)
     oo=pd.DataFrame.from_records(dataset,columns=labels)
     print(oo.head())
     print("Convert to .csv file?(y/n)")
     user_input=input(">")
     if user_input=='y' or user_input=="Y":
         print("Enter name of the .csv file(no need to write .csv)")
         filename=input('>')
         oo.to_csv(f"{filename}.csv")
     #print(len(tweets)==len(sentiment)==len(subjectivity))
     #print("Total number of tweets",len(tweets))
     try:
            print("1.Go back")
            user=int(input('>'))
            if user==1:
             menu()
            else:
             print("That input is invalid, but i'll just take you to the main menu.")
             time.sleep(2)
             menu()
     except:
         print("Oops",sys.exc_info()[0],"ocurred")
         print("Going back to menu...")
         menu()
def menu():
    #Menu Screen
    print("")
    print("")
    print("(that cool banner was just for a good first impression, I think showing it repeatedly is a bit much.")
    print("1.Summon a Boy of Silence (Twitter Sentimantal Analysis)")
    print("2.Who are the Boys of Silence? ")
    userinput=int(input('>'))
    if userinput==1:
     ears()
    elif userinput==2:
     print("""
                    “My children are without blame, without fault -- and without choice.”
                                                                           -The Summoner

     Boys of Silence are outfitted in blue suits that are reminiscent of a school uniform. 
     Their most noticeable feature is their large metal helmets, which amplifies their hearing but obscures their face. 
     These helmets have been fitted onto leather shoulder straps, fastened on by metal clamps, and padlocked shut. 
     Apparently fitted with their uniforms early in life (and have since outgrown them), 
     their blazer sleeves are too short for their arms and their trousers have torn, 
     despite being called "Boys", their hands show apparent deterioration of advanced age.
     The Boys of Silence do not actually engage in combat. 
     Their primary purpose is to keep watch over the realm of Twitter. 
     
     """)
     print("1.Go back")
     user=int(input('>'))
     if user==1:
         menu()
     else:
         print("I don't think that's an option but I assume you wanted to go back so I'll just take you to the menu screen")
         time.sleep(2)
         print("Hold on I'll just get some things..")
         time.sleep(3)
         print("Alright, lets go...")
         time.sleep(1)
         menu()
    else:
     print("I'm sorry I don't understand what that option means")
     print("Try again")
     time.sleep(2)
     menu()
###################################################################################################################################################################
print("""
            .-'''-                                  '''-.                                                                               _..._                        
           '   _    \                             '   _    \                                  .---.                                   .-'_..._''.                     
/|       /   /` '.   \                          /   /` '.   \                             .--.|   |      __.....__        _..._     .' .'      '.\     __.....__      
||      .   |     \  '.-.          .-          .   |     \  '   _.._                      |__||   |  .-''         '.    .'     '.  / .'            .-''         '.    
||      |   '      |  '\ \        / /          |   '      |  '.' .._|                     .--.|   | /     .-''"'-.  `. .   .-.   .. '             /     .-''"'-.  `.  
||  __  \    \     / /  \ \      / /           \    \     / / | '                         |  ||   |/     /________\   \|  '   '  || |            /     /________\   \ 
||/'__ '.`.   ` ..' /    \ \    / /             `.   ` ..' /__| |__                   _   |  ||   ||                  ||  |   |  || |            |                  | 
|:/`  '. '  '-...-'`      \ \  / /                 '-...-'`|__   __|                .' |  |  ||   |\    .-------------'|  |   |  |. '            \    .-------------' 
||     | |                 \ `  /                             | |                  .   | /|  ||   | \    '-.____...---.|  |   |  | \ '.          .\    '-.____...---. 
||\    / '                  \  /                              | |                .'.'| |//|__||   |  `.             .' |  |   |  |  '. `._____.-'/ `.             .'  
|/\'..' /                   / /                               | |              .'.'.-'  /     '---'    `''-...... -'   |  |   |  |    `-.______ /    `''-...... -'    
'  `'-'`                |`-' /                                | |              .'   \_.'                               |  |   |  |             `                      
                         '..'                                 |_|                                                      '--'   '--'                                    
                         """)
print("(^ pretty cool banner huh?)")
print('*'*19)
print("Twitter Sentiments Analyzer v_1.0 by Hamza Ali")
print('*'*19) 
    
print("1.Summon a Boy of Silence (Twitter Sentimantal Analysis)")
print("2.Who are the Boys of Silence? ")
userinput=int(input('>'))
if userinput==1:
    ears()
elif userinput==2:
    print("""
                    “My children are without blame, without fault -- and without choice.”
                                                                           -The Summoner

     Boys of Silence are outfitted in blue suits that are reminiscent of a school uniform. 
     Their most noticeable feature is their large metal helmets, which amplifies their hearing but obscures their face. 
     These helmets have been fitted onto leather shoulder straps, fastened on by metal clamps, and padlocked shut. 
     Apparently fitted with their uniforms early in life (and have since outgrown them), 
     their blazer sleeves are too short for their arms and their trousers have torn, 
     despite being called "Boys", their hands show apparent deterioration of advanced age.
     The Boys of Silence do not actually engage in combat. 
     Their primary purpose is to keep watch over the realm of Twitter. 
     
     """)
    print("1.Go back")
    user=int(input('>'))
    if user==1:
     menu()
    else:
        print("I don't think that's an option but I assume you wanted to go back so I'll just take you to the menu screen")
        time.sleep(2)
        print("Hold on I'll just get some things..")
        time.sleep(3)
        print("Alright, lets go...")
        time.sleep(1)
        menu()

