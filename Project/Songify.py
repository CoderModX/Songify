from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import sys
import pprint
import json
import csv
import emoji
import pandas as pd
import os
import time

client_id='04cef5a228844087991c6993f9ce061c'
client_secret='2efeeab021664d499c4454ab61cd046b'
redirect_uri='https://example.com/callback/'

print(""" ==============   MENU   ==============
            0.EXIT
            
            1.Album Name of Artist
            2.ALBUM URL
            3.Artist ID
            4.DATA TABLE
            5.Preview of Top 10 Songs of Given Artist
            6.Featured Songs of Artist
            7.My Playlist
            8.Top artists of user
            9.Newly Released Songs
            10.User Info
            
======================================""")


search_str = input("\n\nSearch [Enter Artist Name] : ")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id,client_secret))  #client authentication with server with client id and secret id
result = sp.search(search_str)      #search the string entered by user

#print(result['tracks']['items'][0].keys())

file_data = open("Data.csv","w")    #opening csv file with mode writing

writer = csv.writer(file_data)      #declaring writer as object variable

writer.writerow(['Album Name','Release Date','Type','URL','Artist Name','Artist Id'])   #writing the name of the following rows for the value of the keys in dict result

for item in result['tracks']['items']:      #iterating the item in result to write the info required in csv
    writer.writerow([item['album']['name'], item['album']['release_date'], item['album']['type'],item['external_urls']['spotify'],  item['artists'][0]['name'], item['artists'][0]['id']])

file_data.close()   #closing the csv file after saving the data

df=pd.read_csv("Data.csv") #Using Panda to read the csv file saved on desktop

print("""\n===== File Created for Data Requested of name Data.csv || Please check the file and extend the row size to see full info.========= 

                                        Do you want to see the Data in Terminal? 

                                                Press Y/N to continue""")

choice1=input() #choice for yes or no

while(choice1=='Y' or choice1=='y'):
    choice2=input("Enter Number to Access Menu Features: ") #choice 2 for menu
    if (choice2=='1'):
        print("\n===============================================================")
        print(df["Album Name"].to_string())
        print("\n===============================================================")
    if(choice2=='2'):
        print("\n===============================================================")
        print("ARTIST ALBUM URL")
        print(df["URL"].to_string())
        print("\n===============================================================")
    if(choice2=='3'):
        print("\n===============================================================")
        print("Artist ID of Following Album")
        print(df["Artist Id"].to_string())
        print("\n===============================================================")
    if(choice2=='4'):
        colnames=[' ']
        data_list=pd.read_csv('Data.csv', names=colnames)
        print("\n===============================================================")
        print(data_list)
        print("\n===============================================================")
    if(choice2=='5'):
        print("\n===============================================================")
        artist_uri_id=[]        #Declaring an empty list for artist id given in file
        artist_uri_id.append(df["Artist Id"].to_dict())     #adding the values of artist id column in dictionary to access the values through keys
        uri_search=df['Artist Id'][0]                       #assigning the value of key 0, to search
        track_uri_id = ('spotify:artist:'+uri_search)       #adding the uri_search variable to spotify:artist:artist_id to search
        print("Artist Id is ",track_uri_id)
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id,client_secret))     #authenticating client
        results = spotify.artist_top_tracks(track_uri_id)       #searching for Top 10 Tracks of the artist
        for track in results['tracks'][:10]:
            print('track    : ' + track['name'])
            print('cover art: ' + track['album']['images'][0]['url'])
            if (track['preview_url']==None):
                print('audio    : ' + str(track['preview_url']))
            else:
                print('audio    : ' + track['preview_url'])
            print()
        print("\n===============================================================")
    if(choice2=='6'):
        print("\n===============================================================")
        print("Featured songs of Artist\n")
        tracks_list = sp.search(q=search_str, limit=50)     #output limit of songs is 50 and cannot be increased
        tids = []   #empty list for track names
        for i, t in enumerate(tracks_list['tracks']['items']):
            print(' ', i, t['name'])
            tids.append(t['uri'])
        print("\n===============================================================")
    if (choice2=='7'):
        scope = 'playlist-read-private' #scope detail assigned
        print("\n===============================================================")
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri,scope=scope)) #Authenticating User account to access user playlist
        my_playlist = sp.current_user_playlists(limit=50)
        for i, item in enumerate(my_playlist['items']):
            print("%d %s" % (i, item['name']))
        print("\n===============================================================")
    if (choice2=='8'):
        scope = 'user-top-read'
        ranges = ['short_term', 'medium_term', 'long_term']
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri,scope=scope))
        print("\n===============================================================")
        print("Top artists of user\n")
        for sp_range in ['short_term', 'medium_term', 'long_term']:
            print("range:", sp_range)
            results = sp.current_user_top_artists(time_range=sp_range, limit=50)
            for i, item in enumerate(results['items']):
                print(i, item['name'])
            print()
        print("\n===============================================================")
    if (choice2=='9'):
        print("\n===============================================================")
        print("Newly Released Songs\n")
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri))
        response = sp.new_releases()
        while response:
            albums = response['albums']
            for i, item in enumerate(albums['items']):
                print(albums['offset'] + i, item['name'])

            if albums['next']:
                response = sp.next(albums)
            else:
                response = None
        print("\n===============================================================")
    if (choice2=='10'):
        print("\n===============================================================")
        print("User Info\n")
        spotify = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id,client_secret,redirect_uri))
        me = spotify.me()
        print("Diplay Name: ",me['display_name'])
        print("Profile URL:",me['external_urls']['spotify'])
        print("No.of Followers: ",me['followers']['total'])
        print("User Id: ",me['id'])
        print("Spotify URI: ",me['uri'])
        print("\n===============================================================")
    if (choice2=='N' or choice2=='n' or choice2=='0'):
        break;
    choice3=input("Refresh Screen?   Y/N : ")
    if(choice3=='Y' or choice3=='y'):
        print("Refreshing Screen in 10 Seconds") #refreshing Screen
    def countdown(t): 
        while t: 
            mins, secs = divmod(t, 60) 
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(timer, end="\r") 
            time.sleep(1) 
            t -= 1
    t=int(10)
    countdown(t)
    os.system('cls')
    print(""" ==============   MENU   ==============
            0.EXIT
            
            1.Album Name of Artist
            2.ALBUM URL
            3.Artist ID
            4.DATA TABLE
            5.Preview of Top 10 Songs of Given Artist
            6.Featured Songs of Artist
            7.My Playlist
            8.Top artists of user
            9.Newly Released Songs
            10.User Info
            
    ======================================""")

            
print("END OF PROGRAM !! THANKS FOR USING :)")
