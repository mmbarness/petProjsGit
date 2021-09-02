import asyncio
from plexapi.server import PlexServer
from plexwebsocket import PlexWebsocket
import json 

#"pip install asyncio, plexwebsocket"

# local_client obtained by going to https://plex.tv/devices.xml, and replace the x's in local_client below with the name of the device you wish to display the information of"
local_client = "<PlexClient:/resources:xxxxxxxxx" #example: "<PlexClient:/resources:MacBook-Pro.local>"
json_file = "./NowPlayingInfo.json"
baseurl = "<plex server address>" #the server address, which I'm assuming you know. If you don't, you can find the server in plex.tv/devices.xml and put down whatever "publicAddress" is
token = "<ur token here>" #token value found in the same place you found the local_client device name. Will literally read like "token=<some string here>"
plex = PlexServer(baseurl, token)

def session_actions(msgtype, data, error):
    sessions = plex.sessions()
    numSessions = (len(sessions))
    for i in sessions:
        client = str(i.players[0])
        if client == local_client:
            print(i)
            music_writer(i, numSessions)
    if sessions == []: 
        null_writer()
        
def music_writer(session, numSessions):
    info = {
            "Track Title": session.title,
            "Album": session.album().title,
            "Artist": session.artist().title, 
            "Sessions": numSessions,
            "playing": "true",
            }
    with open(json_file, 'w') as outfile:
        json.dump(info, outfile)
    
def null_writer():
    info = {
            "Nothing Playing": "", 
            "playing": "false"
            }
    with open(json_file, 'w') as outfile:
        json.dump(info, outfile)

async def main():
    ws = PlexWebsocket(plex, session_actions, subscriptions=["playing"])
    await ws.listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
