# Youtube-automations

A basic python program written which uses web scrapping and YouTube API to perform certain functions such as downloading a video/playlist, and accessing the data about the video and the playlist, amongst some other things. I do not intend to add any more features to this program. This project was done for my personal convenience of downloading YouTube videos and playlists in bulk, and learn about web scrapping and APIs.

# Dependencies

Before running the program, the user needs to generate a YouTube API key to use the resources of the YouTube API. The user can generate the API key by following the steps given below:
1. Go to the link https://console.developers.google.com/
2. Create a new project
3. Go to the library section and enable the YouTube Data API v3
4. Go to the credentials section and create a new API key
5. Copy the API key and paste it in the `config.py` file in the `API_KEY` variable. This will allow the program to use the resources of the YouTube API.

The program makes use of python libraries- pytube and requests.
Command to download both the libraries

1. pip install pytube
2. pip install requests

# How to run the program

After downloading the libraries, the user needs to run the program by using the command 'python main.py' in the terminal.
