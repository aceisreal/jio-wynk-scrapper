#!/usr/bin/env python
# coding: utf-8

# In[3]:


import subprocess,time,datetime,re,os
required_packages=['requests','pandas','numpy','bs4','requests_futures']
for package in required_packages:
    try:
        subprocess.check_output(['pip', 'show', package])
    except subprocess.CalledProcessError:
        subprocess.call(['pip', 'install', package])
import concurrent.futures,requests,pandas as pd,numpy as np,datetime
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
s = requests.Session()
try:
    response = s.get('https://www.jiosaavn.com/') # Send a GET request to the JioSaavn website
except requests.exceptions.ConnectionError:
    print('Check your internet connection or rerun the code') # Handle connection errors
soup = BeautifulSoup(response.content, 'html.parser') # Parse the HTML content of the response
links = soup.find_all('a',{'class':'u-ellipsis u-color-js-gray'}) # Find all anchor tags with specified class
hrefs = ['https://www.jiosaavn.com'+link.get('href') for link in links] # Extract the href attribute from the anchor tags
songlist=[] # Initialize an empty list to store song data
# Get user input
while True:
    try:
        userinput = int(input('Enter 1 for homepage featured  (JioSaavn)\nEnter 2 for homepage albums (Jiosaavn)\nEnter 3 for homepage songs (Jiosaavn)\nEnter 4 for URL playlists (JioSaavn)\nEnter 5 for URL albums (JioSaavn)\nEnter 6 for playlists (Wynk)\nEnter 7 for albums (Wynk)\n'))
        if userinput not in [1, 2, 3,4,5,6,7]:
            raise ValueError('Invalid input')
        break
    except ValueError:
        print('Invalid input. Please enter between 1-7.')

# Perform actions based on user input
if userinput == 1:
    featuredurls = [i for i in hrefs if i.split('/')[3] == 'featured']
    featured_tokens = [*set(i.split('/')[-1] for i in featuredurls)]
    links = [f'https://www.jiosaavn.com/api.php?__call=webapi.get&token={i}&type=playlist&p={j}&n=50&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0' for i in featured_tokens for j in range(1, 3)]
    def fetch_songs(link):
        try:
            r = s.get(link)
        except requests.exceptions.ConnectionError:
            print('Check your internet connection or rerun the code.')
            return []
        try:
            song_info=r.json()
            song_inner_info=r.json()['list']
            playlist_title = song_info['title']
            playlist_fancount = song_info['more_info']['fan_count']
            songs = []
            for i in range(len(song_inner_info)):
                song_data = {
                    'Song Name':song_inner_info[i]['title'],
                    'Song Len':song_inner_info[i]['more_info']['duration'],
                    'Song PlayCount':song_inner_info[i]['play_count'],
                    'Song Album':song_inner_info[i]['more_info']['album'],
                    'Song Label':song_inner_info[i]['more_info']['copyright_text'],
                    'Song Language':song_inner_info[i]['language'],
                    'Song Release Date':song_inner_info[i]['more_info']['release_date'],
                    'Song Playlist': playlist_title,
                    'Playlist Fancount': playlist_fancount,
                    'Song Artist': song_inner_info[i]['more_info']['artistMap']['artists'][0]['name'] if len(song_inner_info[i]['more_info']['artistMap']['artists']) > 0 else None,
                    'Song Artist1': song_inner_info[i]['more_info']['artistMap']['artists'][1]['name'] if len(song_inner_info[i]['more_info']['artistMap']['artists']) > 1 else None,
                    'Song Artist2': song_inner_info[i]['more_info']['artistMap']['artists'][2]['name'] if len(song_inner_info[i]['more_info']['artistMap']['artists']) > 2 else None
                }
                try:
                    songs.append(song_data)
                except:
                    pass
            return songs
        except:
            return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(fetch_songs, link) for link in links]
        for future in concurrent.futures.as_completed(futures):
            try:
                songlist += future.result()
            except:
                pass
elif userinput == 2:
    albumurls=[i for i in hrefs if i.split('/')[3]=='album']
    albumtokens=[i.split('/')[-1] for i in albumurls]
    links = [f'https://www.jiosaavn.com/api.php?__call=webapi.get&token='+i+'&type=album&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0' for i in albumtokens]
    def fetch_songs(link):
        try:
            r = s.get(link)
        except requests.exceptions.ConnectionError:
            print('Check your internet connection or rerun the code.')
            return []
        try:
            song_in=r.json()['list']
            songs = []
            for i in range(len(song_in)):
                song_data={
                    'Song Name':song_in[i]['title'],
                    'Song Len':song_in[i]['more_info']['duration'],
                    'Song PlayCount':song_in[i]['play_count'],
                    'Song Album':song_in[i]['more_info']['album'],
                    'Song Year':song_in[i]['more_info']['release_date'],
                    'Song Label':song_in[i]['more_info']['copyright_text'],
                    'Song Language':song_in[i]['language'],
                    'Song Release Date':song_in[i]['more_info']['release_date'],
                    'Song Artist': song_in[i]['more_info']['artistMap']['artists'][0]['name'] if len(song_in[i]['more_info']['artistMap']['artists']) > 0 else None,
                    'Song Artist1': song_in[i]['more_info']['artistMap']['artists'][1]['name'] if len(song_in[i]['more_info']['artistMap']['artists']) > 1 else None,
                    'Song Artist2': song_in[i]['more_info']['artistMap']['artists'][2]['name'] if len(song_in[i]['more_info']['artistMap']['artists']) > 2 else None
                }
                try:
                    songs.append(song_data)
                except:
                    pass
            return songs
        except:
            return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(fetch_songs, link) for link in links]
        for future in concurrent.futures.as_completed(futures):
            try:
                songlist += future.result()
            except:
                pass
elif userinput == 3:
    songurls=[i for i in hrefs if i.split('/')[3]=='song']
    songtokens=[i.split('/')[-1] for i in songurls]
    links = [f'https://www.jiosaavn.com/api.php?__call=webapi.get&token='+i+'&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0' for i in songtokens]
    def fetch_songs(link):
        try:
            r = s.get(link)
        except requests.exceptions.ConnectionError:
            print('Check your internet connection or rerun the code.')
            return []
        try:
            song_in=r.json()['songs']
            songs = []
            for i in range(len(song_in)):
                song_data={
                        'Song Name':song_in[i]['title'],
                        'Song Len':song_in[i]['more_info']['duration'],
                        'Song PlayCount':song_in[i]['play_count'],
                        'Song Album':song_in[i]['more_info']['album'],
                        'Song Year':song_in[i]['year'],
                        'Song Language':song_in[i]['language'],
                        'Song Artist': song_in[i]['more_info']['artistMap']['artists'][0]['name'] if len(song_in[i]['more_info']['artistMap']['artists']) > 0 else None,
                        'Song Artist1': song_in[i]['more_info']['artistMap']['artists'][1]['name'] if len(song_in[i]['more_info']['artistMap']['artists']) > 1 else None,
                        'Song Artist2': song_in[i]['more_info']['artistMap']['artists'][2]['name'] if len(song_in[i]['more_info']['artistMap']['artists']) > 2 else None
                         }
                try:
                    songs.append(song_data)
                except:
                    pass
            return songs
        except:
            return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(fetch_songs, link) for link in links]
        for future in concurrent.futures.as_completed(futures):
            try:
                songlist += future.result()
            except:
                pass
elif userinput==4:
    jiosaavn_url=input(str('Enter the link of the playlist: '))
    jiosaavn_split=jiosaavn_url.split('/')
    playlist_token=jiosaavn_split[5]
    r=s.get('https://www.jiosaavn.com/api.php?__call=webapi.get&token='+playlist_token+'&type=playlist&p=1&n=50&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0')
    r1=r.json()
    playlist_id=r1['id']
    final_url='https://saavn.me/playlists?id='+playlist_id
    songlist=[]
    url=final_url
    r=s.get(str(url))
    song_in=r.json()['data']['songs']
    for i in range(len(song_in)):
            song_data={
                'Song Name':song_in[i]['name'],
                'Song Len':song_in[i]['duration'],
                'Song PlayCount':song_in[i]['playCount'],
                'Song Album':song_in[i]['album']['name'],
                'Song Year':song_in[i]['releaseDate'],
                'Song Artist':song_in[i]['primaryArtists'],
                'Song Label':song_in[i]['copyright'],
                'Song Language':song_in[i]['language']
            }
            songlist.append(song_data)
elif userinput==5:
    a_url=str(input("Enter the link of the album: "))
    final_url='https://saavn.me/albums?link='+a_url
    songlist=[]
    url=final_url
    r=s.get(str(url))
    songs_json=r.json()
    songs_data=songs_json['data']
    try:
        song_in=songs_data['songs']
        for i in range(len(song_in)):
            song_data={
                  'Song Title':song_in[i]['name'],
                  'Song Duration':song_in[i]['duration'],
                  'Song PlayCount':song_in[i]['playCount'],
                  'Song Album':song_in[i]['album']['name'],
                  'Song Year':song_in[i]['releaseDate'],
                  'Song Artist':song_in[i]['primaryArtists'],
                  'Song Label':song_in[i]['copyright'],
                  'Song Language':song_in[i]['language']
                  }
            songlist.append(song_data)
    except:
        pass
elif userinput==6:
    wynk_url = input(str('Enter the link of the playlist: '))
    wynk_split = re.split('/|_', wynk_url)
    type_of_release = wynk_split[4]
    playlist_token = wynk_split[7].split('?')[0]
    numbers = range(0, 520, 20)

    def get_songs(offset):
        url = f'https://content.wynk.in/music/v4/content?id=srch_bsb_{playlist_token}&type={type_of_release.upper()}&offset={offset}&count=20&contentLangs=hi,en'
        response = s.get(url)
        songs = []
        if response.ok:
            data = response.json()
            for item in data['items']:
                song = {
                    'Song Title': item['title'],
                    'Song Duration': item['duration'],
                    'Song Album': item['album'],
                    'Song Artist': item['singers'][0]['title'] if item['singers'] else ''
                }
                songs.append(song)
        return songs

    with ThreadPoolExecutor() as executor:
        songs = executor.map(get_songs, numbers)

    songlist = [song for sublist in songs for song in sublist]
elif userinput==7:
    link=str(input('Enter the url: '))
    response = s.get(link)
    page = BeautifulSoup(response.content, 'html.parser')
    songs = page.find_all('a',{'class':'jsx-7c093e1a359b5feb text-title font-normal line-clamp-1 md:line-clamp-2 text-sm hover:underline'})
    artists = page.find_all('div',{'class':"jsx-7c093e1a359b5feb line-clamp-2 text-sm"})
    song_len = page.find_all('div',{'class':'jsx-7c093e1a359b5feb hidden text-sm leading-4 font-normal w-[15%] md:w-[18%] lg:w-[12%] max-w-4xl md:line-clamp-1 text-wynk-static-black dark:text-wynk-white60'})
    songlist={'Song Title':[song.text for song in songs],'Song Artist':[artist.text for artist in artists],
                               'Song Duration':[sl.text for sl in song_len]}

# Define a dictionary to map user input to corresponding file prefixes
prefix_mapping = {
    1: "homepage_featured",
    2: "homepage_albums",
    3: "homepage_songs",
    4: "URL_playlists",
    5: "URL_albums",
    6: "playlists_Wynk",
    7: "albums_Wynk"
}

# Get the prefix based on user input
prefix = prefix_mapping.get(userinput)

# Check if a valid prefix is found
if prefix is None:
    print("Invalid user input. Please try again.")
    exit()

try:
    df=pd.DataFrame(songlist)
    df.index = np.arange(1, len(df) + 1)
    df['Song Len'] = pd.to_numeric(df['Song Len'], errors='coerce')
    df['datetime'] = pd.to_datetime(df['Song Len'], unit='s')
    df['Song Length '] = df['datetime'].dt.strftime('%M:%S')
    df.insert(1, 'Song Length', df['Song Length '])
    df.drop(columns={'Song Length ','Song Len','datetime'},inplace=True)
    df['Song PlayCount']=pd.to_numeric(df['Song PlayCount'])
    df['Song PlayCount'] = df['Song PlayCount'].apply(lambda x: '{:,.0f}'.format(x))
    df['Song Artist1'].replace(np.nan,'',inplace=True)
    df['Song Artist2'].replace(np.nan,'',inplace=True)
    df['Song Creators']=df['Song Artist']+', '+df['Song Artist1']+', '+df['Song Artist2']
    df['Song Creators'] = df['Song Creators'].apply(lambda x: ', '.join(set(x.split(', '))))
    df['Song Creators'] = df['Song Creators'].str.strip(', ')
    df.drop(columns={'Song Artist','Song Artist1','Song Artist2'},inplace=True)
except:
    pass
try:
    df.index = np.arange(1, len(df) + 1)
    df['datetime'] = pd.to_datetime(df['Song Duration'], unit='s')
    df['Song Length '] = df['datetime'].dt.strftime('%M:%S')
    df.insert(1, 'Song Length', df['Song Length '])
    df.drop(['Song Length '],axis=1,inplace=True)
    df.drop(['Song Duration'],axis=1,inplace=True)
    df.drop(['datetime'],axis=1,inplace=True)
except:
    pass
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
desktop_path = os.path.expanduser("~/Desktop")
filename = os.path.join(desktop_path, f"{prefix}_{timestamp}.csv")
df.to_csv(filename,index=False)


# In[ ]:




