import asyncio
from plexapi.server import PlexServer
from plexwebsocket import PlexWebsocket, SIGNAL_CONNECTION_STATE
import json 

#"pip install asyncio, plexwebsocket"

# local_client obtained by printing "plex.sessions.players in this file, then running it"
local_client = "<PlexClient:/resources:xxxxxxxxx"
json_file = "./NowPlayingInfo.json"
baseurl = "<plex server address>"
token = "<ur token here>"
plex = PlexServer(baseurl, token)

def session_actions(msgtype, data, error):
    sessions = plex.sessions()
    numSessions = (len(sessions))
    for i in sessions:
        client = str(i.players[0])
        if client == local_client:
            music_writer(i, numSessions)
    if sessions == []: 
        null_writer()
        
def music_writer(session, numSessions):
    info = {"Track Title": session.title,
                  "Album": session.album().title,
                  "Artist": session.artist().title, 
                  "Sessions": numSessions
                  }
    with open(json_file, 'w') as outfile:
        json.dump(info, outfile)
    
def null_writer():
    info = {"Nothing Playing": ""}
    with open(json_file, 'w') as outfile:
        json.dump(info, outfile)

async def main():
    ws = PlexWebsocket(plex, session_actions, subscriptions=["playing"])
    await ws.listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
