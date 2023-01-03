# contains helper functions for the main.py file and youtube.py file

# convert time to string format
def convert_time_to_string(durationHours, durationMinutes, durationSeconds):
    durationMinutes += durationSeconds//60
    durationSeconds = durationSeconds%60
    durationHours += durationMinutes//60
    durationMinutes = durationMinutes%60
    #make sure that the duration is in the format HH:MM:SS
    if (durationHours < 10):
        durationHours = "0" + str(durationHours)
    if (durationMinutes < 10):
        durationMinutes = "0" + str(durationMinutes)
    if (durationSeconds < 10):
        durationSeconds = "0" + str(durationSeconds)
    duration = str(durationHours) + ":" + str(durationMinutes) + ":" + str(durationSeconds)
    return duration

# convert string to time format
def get_formatted_time(videoDuration):
    videoDuration = videoDuration.replace("PT", "")
    if ("H" not in videoDuration):
        videoDuration = "0:" + videoDuration
    else:
        videoDuration = videoDuration.replace("H", ":")
    if ("M" not in videoDuration):
        videoDuration = videoDuration + ":00"
    else:
        videoDuration = videoDuration.replace("M", ":")
    if ("S" not in videoDuration):
        videoDuration = videoDuration + "00"
    else:
        videoDuration = videoDuration.replace("S", "")
    videoDuration = videoDuration.split(":")
    return videoDuration

# format the number to have commas for better readability
def get_formatted_numbers(number):
    number = str(number)
    if (len(number) > 3):
        number = number[::-1]
        number = ",".join(number[i:i+3] for i in range(0, len(number), 3))
        number = number[::-1]
    return number

# format the date to DD/MM/YYYY
def get_formatted_date(date):
    date = date.split("T")[0]
    date = date.split("-")
    date = date[2] + "/" + date[1] + "/" + date[0]
    return date