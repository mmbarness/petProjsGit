this little tool opens a websocket to your plex server using the python package plexapi, then writes the media playback information of a device of your choosing to a json file. a very small node server can be run that responds to a couple endpoints, the most important one of which returns a neatly packaged string reflecting whatever's currently being written to the json file. I've found using pm2 to run the node server in the background is the easiest way to automate the whole thing, so that I have no need to start anything when I boot up my computer - see their github for more info on that front. If everything's running correctly, all you should need to put into Better Touch Tool is "curl -s http://localhost:8000/gimme". The -s flag prevents default curl behavior that prints out unnecessary information IF nothing is otherwise returned.