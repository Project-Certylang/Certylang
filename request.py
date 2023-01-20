from spotifysearch.client import Client
# Then, we create an instance of that class passing our credentials as arguments.
# IMPORTANT: Don't put your credentials inside your code if your planning to publish it.

client_id = "e7f49f1b335940b3abffbf76fa8332d2"
client_secret = "2e9e321b25ad4176935fe31f92779c73"

myclient = Client(client_id, client_secret)

# Now we can call the method search() from our client and store the results in a new object.
results = myclient.search("곡예사")

# Then we call the method get_tracks() from our results object, which returns a list of tracks.
tracks = results.get_tracks()

# Now, let's access the first track in our list by using index 0.
track = tracks[0]

# Finally, we can access some information contained in our track.
code = track.url.split("/")[4]
print(code)
uri = 'spotify:track:'+code
# print(track.name, "-", track.artists[0].name)
# print(track.url)