import youtube as yt
def main():
    while (True):
        print("Following options are available:")
        print("1. Get playlist duration")
        print("2. Get playlist details")
        print("3. Get playlist videos titles")
        print("4. Get video details")
        print("5. Download video in mp4 format")
        print("6. Check if video exists in playlist")
        print("7. Download playlist videos in mp4 format")
        print("8. Download playlist videos in mp3 format")
        print("9. Download a video in mp3 format")
        print("10. Exit")
        choice = int(input("Enter your choice: "))
        if (choice in [4,5,9]):
            url = input("Enter video URL: ")
            if (choice == 4):
                yt.get_video_details(url)
            elif (choice == 9):
                yt.download_video_mp3(url)
            else:
                yt.download_video(url)
        elif (choice in [1,2,3,7,8]):
            url = input("Enter playlist URL: ")
            if (choice == 1):
                yt.get_playlist_duration(url)
            elif (choice == 2):
                yt.get_playlist_details(url)
            elif (choice == 3):
                yt.get_playlist_videos(url)
            elif (choice == 8):
                yt.download_playlist_mp3(url)
            else:
                yt.download_playlist(url)
        elif (choice == 6): 
            videoURL = input("Enter video URL: ")
            playlistURL = input("Enter playlist URL: ")
            yt.check_video_in_playlist(videoURL, playlistURL)
        else:
            print("Thank you for using this program")
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
