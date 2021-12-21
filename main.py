from pytube import YouTube, Playlist
import os
from ytmusicapi import YTMusic

def authenticate():
    #copy entire 'POST' headers from firefox by browsing '/browse' in network lists and follow commands from pop up terminals
    YTMusic.setup(filepath="headers_auth.json")


def convert(urlList):
    counter = 1
    for url in urlList:
        yt = YouTube(url)
        yt.streams.filter()
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path="desired output path...")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print(f'dowonloaded...{counter}/{len(urlList)}')
        counter+=1

def getPlaylist():
    print("setting up...")
    ytmusic = YTMusic('headers_auth.json')
    trackList = ytmusic.get_liked_songs(limit=5000).get('tracks')
    urlList = []
    for track in trackList:
        urlLink = 'https://www.youtube.com/watch?v='
        videoId = str(track.get('videoId'))
        urlLink += videoId
        urlList.append(urlLink)
    print("download starting...")
    return urlList

def downloadAllSongs():
    urlList = getPlaylist()
    convert(urlList)
    print("download finished")

if __name__ == '__main__':
    downloadAllSongs()

