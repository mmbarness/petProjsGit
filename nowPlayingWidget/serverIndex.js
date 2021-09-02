const fp = require('find-process')
const {PythonShell} = require('python-shell')

const http = require('http');
const { fstat, readFileSync, readFile } = require('fs');
const host = 'localhost';
const port = 8000;

const requestListener = async (req, res) => {
    res.setHeader("Content-Type", "application/json");
    switch (req.url) {
        case "/gimme": //basically the one endpoint you need to worry about. returns info if the python script is already running and starts the script if its not, then returns the info.
            res.writeHead(200);
            let returnVal = await manager();
            res.end(returnVal)
            break
        case "/kill": //just in case you need to call this, for whatever reason. kills whatever instances of the python script are running
            res.writeHead(200);
            let pid = await kill(); 
            res.end(`killed ${pid}`)
            break
        default: 
            res.writeHead(404);
            res.end('invalid endpoint')
    }
}

const manager = async () => {
    let pyProcess = await findPythonPID()
    if (pyProcess.running) { //if it finds the python script is already running, it returns the result of nowPlaying
        return nowPlaying()
    } else {
        let process = PythonShell.run('./nowPlaying.py', null ) //uses the python shell node package to initalize the python script that actually opens the websocket and writes to json
        pyProcess = findPythonPID()
        return nowPlaying();
    }
}

const nowPlaying = () => {
    let json_file = readFileSync("./nowPlayingInfo.json")
    let NOWPLAYING_JSON = JSON.parse(json_file)
    if (NOWPLAYING_JSON.playing === 'true'){ //the script can be running while nothing is playing, so "playing: false" is therefore in those circumstances written to the json
        return(`${NOWPLAYING_JSON['Track Title']} | ${NOWPLAYING_JSON['Artist']} | Sessions: ${NOWPLAYING_JSON['Sessions']}`)
    } else {
        return (' ')
    }
}

const kill = async () => {
    let pidInfo = await findPythonPID()
    if (!pidInfo.running) {return 'no scripts currently running'}
    if (pidInfo.processes.length > 1){
        for (pyProcess of pidInfo.processes){
            process.kill(pyProcess.pid)
        }
    } else if (pidInfo.processes.length === 1){
        process.kill(pidInfo.processes[0].pid)
    }
}

const server = http.createServer(requestListener)

server.listen(port, host, () => {
    console.log('yep, its runnin')
})

const findPythonPID = async () => {
    let pidPromise = await fp('name', 'nowPlaying.py') // search for any process with "nowPlaying.py in the name and assign to variable"
    if (pidPromise.length === 1) {
        return {running: true, processes: pidPromise}
    } else if (pidPromise.length > 1) {
        return {running: true, processes: pidPromise}
    } else {
        return {running: false, processes: []}
    }
}

