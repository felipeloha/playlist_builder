from telegram_reader import telegram, read_messages
from spotify_handler import spotify, search_song

telegram = telegram()
titles = read_messages(telegram)
titles = list(filter(lambda item: item, titles))
print(titles)

spotify = spotify()

for title in titles:
    print("searching ", title)
    track = search_song(spotify, title)
    print(track)

#todo clean none and other invalid inputs
#todo search music in spotify
#todo add music to playlist
