import json
from pytube import YouTube
import os
from googleapiclient.discovery import build
import requests
import helper as helper

SERVICE_NAME = "youtube"
API_VERSION = "v3"
API_KEY = "AIzaSyCTw2BGfyjyCp_JlILhm9Q_vDW3hofZgeg"
youtube = build(SERVICE_NAME, API_VERSION, developerKey = API_KEY)

#get the details of a video
def get_video_details(url):
    if (check_video_exists(url)):
        videoURL = url.split("v=")[1]
        #access the snippets, contentDetails and statistics of the video
        videoRequest = youtube.videos().list(part = "snippet, statistics, contentDetails", id = videoURL)
        videoResponse = videoRequest.execute()
        videoTitle = videoResponse['items'][0]['snippet']['title']
        channelName = videoResponse['items'][0]['snippet']['channelTitle']
        videoDuration = videoResponse['items'][0]['contentDetails']['duration']
        videoDuration = helper.get_formatted_time(videoDuration)
        videoDuration = helper.convert_time_to_string(int(videoDuration[0]), int(videoDuration[1]), int(videoDuration[2]))
        videoViews = videoResponse['items'][0]['statistics']['viewCount']
        videoViews = helper.get_formatted_numbers(videoViews)
        videoLikes = videoResponse['items'][0]['statistics']['likeCount']
        videoLikes = helper.get_formatted_numbers(videoLikes)
        videoComments = videoResponse['items'][0]['statistics']['commentCount']
        videoComments = helper.get_formatted_numbers(videoComments)
        videoUploadDate = videoResponse['items'][0]['snippet']['publishedAt']
        videoUploadDate = helper.get_formatted_date(videoUploadDate)
        print("Video Upload Date:", videoUploadDate)
        print("Video Title:", videoTitle)
        print("Channel Name:", channelName)
        print("Video Duration:", videoDuration)
        print("Video Views:", videoViews)
        print("Video Likes:", videoLikes)
        print("Video Comments:", videoComments)
    else:
        print("Requested video does not exist")

#calculate the total duration of all videos in a playlist
def get_playlist_duration(url):
    if (check_playlist_exists(url)):
        playlistURL = url.split("list=")[1]
        playlist_request = youtube.playlists().list(part = "snippet", id = playlistURL)
        playlist_response = playlist_request.execute()
        playlist_title = playlist_response['items'][0]['snippet']['title']
        print("Playlist Title:", playlist_title)
        nextPage = None
        durationHours = 0
        durationMinutes = 0
        durationSeconds = 0
        while True:
            playlistRequest = youtube.playlistItems().list(part = "snippet", playlistId = playlistURL, maxResults = 50, pageToken = nextPage)
            playlistResponse = playlistRequest.execute()
            for item in playlistResponse['items']:
                videoID = item['snippet']['resourceId']['videoId']
                videoRequest = youtube.videos().list(part = "contentDetails", id = videoID)
                videoResponse = videoRequest.execute()
                videoDuration = videoResponse['items'][0]['contentDetails']['duration']
                videoDuration = helper.get_formatted_time(videoDuration)
                durationHours += int(videoDuration[0])
                durationMinutes += int(videoDuration[1])
                durationSeconds += int(videoDuration[2])
            nextPage = playlistResponse.get('nextPageToken')
            if nextPage is None:
                break
        totalDuration = helper.convert_time_to_string(durationHours, durationMinutes, durationSeconds)
        print("Total Duration:", totalDuration)
    else:
        print("Requested playlist does not exist")

#prints the title of all videos in the playlist
def get_playlist_videos(url):
    if (check_playlist_exists(url)):
        playlistURL = url.split("list=")[1] 
        nextPage = None
        count = 1
        while True:
            playlistRequest = youtube.playlistItems().list(part = "snippet", playlistId = playlistURL, maxResults = 50, pageToken = nextPage)
            playlistResponse = playlistRequest.execute()
            for item in playlistResponse['items']:
                print(str(count)+".", item['snippet']['title'])
                print(item['snippet']['resourceId']['videoId'])
                count += 1
            nextPage = playlistResponse.get('nextPageToken')
            if nextPage is None:
                break
    else:
        print("Requested playlist does not exist")
#prints the details of the playlist
def get_playlist_details(url):
    if (check_playlist_exists(url)):
        playlistURL = url.split("list=")[1]
        playlistRequest = youtube.playlists().list(part = "snippet, contentDetails", id = playlistURL)
        playlistResponse = playlistRequest.execute()
        playlistTitle = playlistResponse['items'][0]['snippet']['title']
        playlistChannel = playlistResponse['items'][0]['snippet']['channelTitle']
        playlistNumberOfVideos = playlistResponse['items'][0]['contentDetails']['itemCount']
        print("Playlist Title:", playlistTitle)
        print("Channel Name:", playlistChannel)
        print("Number of Videos:", playlistNumberOfVideos)
        get_playlist_duration(url)
    else:
        print("Requested playlist does not exist")

def check_video_exists(videoURL):
    try:
        videoURL = videoURL.split("v=")[1]
    except:
        return False
    videoRequest = youtube.videos().list(part = "snippet", id = videoURL)
    videoResponse = videoRequest.execute()
    if len(videoResponse['items']) == 0:
        return False
    else:
        return True

def check_playlist_exists(playlistURL):
    try:
        playlistURL = playlistURL.split("list=")[1]
    except:
        return False
    playlistRequest = youtube.playlists().list(part = "snippet", id = playlistURL)
    playlistResponse = playlistRequest.execute()
    if len(playlistResponse['items']) == 0:
        return False
    else:
        return True

def check_video_in_playlist(videoURL, playlistURL):
    nextPage = None
    if (check_video_exists(videoURL)==False):
        print("Requested video does not exist")
        return False
    if (check_playlist_exists(playlistURL)==False):
        print("Requested playlist does not exist")
        return False
    playlistURL = playlistURL.split("list=")[1]
    videoURL = videoURL.split("v=")[1]
    while True:
        playlistRequest = youtube.playlistItems().list(part = "snippet", playlistId = playlistURL, maxResults = 50, pageToken = nextPage)
        playlistResponse = playlistRequest.execute()
        for item in playlistResponse['items']:
            if item['snippet']['resourceId']['videoId'] == videoURL:
                print("Video exists in the given playlist")
                return True
        nextPage = playlistResponse.get('nextPageToken')
        if nextPage is None:
            break
    print("Video does not exist in playlist")
    return False

def download_video(url):
    if (check_video_exists(url)):
        yt = YouTube(url)
        print("Downloading video with title:", yt.title)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        print("Downloaded video successfully")

#downloads video in mp3 format
def download_video_mp3(url):
    if (check_video_exists(url)):
        yt = YouTube(url)
        print("Downloading video in mp3 format with title:", yt.title)
        yt.streams.filter(only_audio=True).first().download()
        print("Downloaded video in mp3 format successfully")

def download_playlist(url):
    if (check_playlist_exists(url)):
        playlistURL = url.split("list=")[1]
        playlist_request = youtube.playlists().list(part = "snippet" , id = playlistURL)
        playlist_response = playlist_request.execute()
        playlist_title = playlist_response['items'][0]['snippet']['title']
        print("Downloading playlist with title:", playlist_title)
        # create a new folder with name of playlist title
        try:
            os.mkdir(playlist_title)
        except OSError:
            print("Could not create the required directory for downloading playlist")
        else:
            try:
                os.chdir(playlist_title)
            except OSError:
                print("Error in changing the current directory")
            else:
                #maintaining a token for the next page
                nextPage = None
                while True:
                    playlist_request = youtube.playlistItems().list(part = "snippet", playlistId = playlistURL, maxResults = 50, pageToken = nextPage)
                    playlist_response = playlist_request.execute()
                    for item in playlist_response['items']:
                        videoURL = "https://www.youtube.com/watch?v=" + item['snippet']['resourceId']['videoId']
                        download_video(videoURL)
                    nextPage = playlist_response.get('nextPageToken')
                    if nextPage is None:
                        print("Downloaded playlist successfully")
                        #changing the current working directory to the parent directory
                        try:
                            os.chdir("..")
                        except OSError:
                            print("Error in changing the current directory")
                        else:
                            break


# downlaods playlist in mp3 format in a new folder with name of folder as playlist title
def download_playlist_mp3(url):
    if (check_playlist_exists(url)):
        playlistURL = url.split("list=")[1]
        playlist_request = youtube.playlists().list(part = "snippet" , id = playlistURL)
        playlist_response = playlist_request.execute()
        playlist_title = playlist_response['items'][0]['snippet']['title']
        print("Downloading playlist in mp3 format with title:", playlist_title)
        # creating a new folder with name of playlist title
        try:
            os.mkdir(playlist_title)
        except OSError:
            print("Could not create the required directory for downloading playlist in mp3 format")
        else:
            # changing the current working directory to the newly created folder
            try:
                os.chdir(playlist_title)
            except OSError:
                print("Error in changing current directory")
            else:
                #maintaing a token for the next page
                nextPage = None
                while True:
                    playlistRequest = youtube.playlistItems().list(part = "snippet", playlistId = playlistURL, maxResults = 50, pageToken = nextPage)
                    playlistResponse = playlistRequest.execute()
                    for item in playlistResponse['items']:
                        videoID = item["snippet"]["resourceId"]["videoId"]
                        videoURL = "https://www.youtube.com/watch?v=" + videoID
                        download_video_mp3(videoURL)
                    nextPage = playlistResponse.get('nextPageToken')
                    if nextPage is None:
                        print("Downloaded playlist in mp3 format successfully")
                        # changing the current working directory to the parent directory
                        try:
                            os.chdir("..")
                        except OSError:
                            print("Error in changing current directory")
                        break
    else:
        print("Requested playlist does not exist")