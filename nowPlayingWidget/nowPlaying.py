import asyncio
from plexapi.server import PlexServer
from plexwebsocket import PlexWebsocket, SIGNAL_CONNECTION_STATE
import json 

baseurl = "<plex server address>"
token = "<ur token here>"
plex = PlexServer(baseurl, token)
local_client = "<PlexClient:/resources:xxxxxxxxx" #obtained by printing "plex.sessions.players in this file, then running it"

def print_info(msgtype, data, error):
    sessions = plex.sessions()
    num_sessions = (len(sessions))
    for i in sessions:
        client = str(i.players[0])
        if client == local_client:
            music_writer(i, num_sessions)

def music_writer(session, num_sessions):
    info = {"Track Title": session.title,
                  "Album": session.album().title,
                  "Artist": session.artist().title, 
                  "Sessions": num_sessions
                  }
    with open('<json filepath>', 'w') as outfile:
        json.dump(info, outfile)

async def main():
    ws = PlexWebsocket(plex, print_info, subscriptions=["playing"])
    await ws.listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
