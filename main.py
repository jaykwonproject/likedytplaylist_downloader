from ytmusicapi import YTMusic
import youtube_dl
import multiprocessing


def authenticate():
    # copy entire 'POST' headers from firefox by browsing '/browse' in network lists and follow commands from pop up terminals
    YTMusic.setup(filepath="headers_auth.json")


def multiThread():
    songList = getPlaylist()
    songs = []
    for song in songList:
        songs.append(song)
    pool = multiprocessing.Pool()
    outputs = pool.map(convert, songs)
    print(outputs)


def convert(song):
    songList = getPlaylist()
    url = songList[song]
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'/Users/jay/Desktop/mus/songs/{song}.',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f'finished downloading : {song}.mp3')


def getPlaylist():
    print("setting up...")
    ytmusic = YTMusic('headers_auth.json')
    trackList = ytmusic.get_liked_songs(limit=5000).get('tracks')
    songList = {}
    for track in trackList:
        urlLink = 'https://www.youtube.com/watch?v='
        videoId = str(track.get('videoId'))
        urlLink += videoId
        title = str(track.get('title'))
        songList[title] = urlLink
    print("download starting...")
    return songList


def saveCurrentplaylist():
    songList = getPlaylist()
    textfile = open("songList.txt", "w")
    for element in songList:
        textfile.write(element + "\n")
    textfile.close()


if __name__ == '__main__':
    saveCurrentplaylist()
    multiThread()
