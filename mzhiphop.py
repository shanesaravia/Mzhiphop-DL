import requests, bs4, os, youtube_dl


# Returns List of Tracks Joined By "+"
def tracks(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text.encode('utf-8').decode('ascii', 'ignore'), 'html.parser')

    searchTracks = soup.select('.update_song_info a')
    prettyTracks = soup.select('.update_song_info a')
    for n, i in enumerate(searchTracks):
        searchTracks[n] = i.getText('').replace('-', '').replace(' ', '+').replace('++', '+')
    for n, i in enumerate(prettyTracks):
        prettyTracks[n] = i.getText('')
    return(searchTracks, prettyTracks)
    
searchList, prettyList = tracks('http://www.mzhiphop.com')


# Returns Selection of Songs
def userSelection(searchList, prettyList):
    for count, i in enumerate(prettyList):
        print(str(count) + ' - ' + i)


    askList = input('Input numbers or "all": \n>')
    if askList == 'all':
           return(searchList)
    else:
        finalList = [int(x) for x in askList.split()]
        userSelection = []
        for n in finalList:
            userSelection.append(searchList[n])
        return(userSelection)

userSelection = userSelection(searchList, prettyList)

# Search Youtube
def youtube(song):
    resYoutube = requests.get('https://www.youtube.com/results?search_query=' + song)
    resYoutube.raise_for_status()
    soupYT = bs4.BeautifulSoup(resYoutube.text.encode('utf-8').decode('ascii', 'ignore'), 'html.parser')
    
    checkForAds = soupYT.find_all('div', {'class': 'pyv-afc-ads-container'})
    if checkForAds == []:
        count = 0
    else:
        count = 2
        
    video = soupYT.find_all('h3', {'class': 'yt-lockup-title'})
    videoHref = video[count].find('a')
    url = 'https://www.youtube.com' + videoHref.attrs['href']
    return(url)

def getURL(userSelection):
    ytList = []
    for n in userSelection:
        ytList.append(youtube(n))
    return(ytList)

urlList = getURL(userSelection)

# Youtube_DL - Download Song
def youtubeDL(url):
    options = {
        'format': 'bestaudio/best', # choice of quality
        'extractaudio' : True,      # only keep the audio
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        'outtmpl': 'C:/Users/Shane Saravia/Music/TrackName/%(title)s.%(ext)s',     # name the file
        'noplaylist' : True,        # only download single song, not playlist
    }
    
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])

for d in urlList:
    youtubeDL(d)