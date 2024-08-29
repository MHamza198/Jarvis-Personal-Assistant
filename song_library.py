# song_library.py
song_list = {
    "unforgettable": "https://www.youtube.com/watch?v=72eQoVgbEG8",
    "song2": "https://www.youtube.com/watch?v=song_link_2",
    "song3": "https://www.youtube.com/watch?v=song_link_3",
    "song4": "https://www.youtube.com/watch?v=song_link_4",
    "song5": "https://www.youtube.com/watch?v=song_link_5",
    "song6": "https://www.youtube.com/watch?v=song_link_6",
    "song7": "https://www.youtube.com/watch?v=song_link_7",
    "song8": "https://www.youtube.com/watch?v=song_link_8",
    "song9": "https://www.youtube.com/watch?v=song_link_9",
    "song10": "https://www.youtube.com/watch?v=song_link_10"
}

def get_song_url(song_name):
    return song_list.get(song_name.lower(), None)
