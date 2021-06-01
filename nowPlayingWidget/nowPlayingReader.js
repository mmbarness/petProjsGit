let json_file = "<absolute path to json file goes here>"
let np_script = "./nowPlaying.py"
let fp = require('find-process')
let {PythonShell} = require('python-shell')

//"npm install find-process, python-shell"

const data = require(json_file)
let pid = ""

const findPythonPID = async () => {
    let pidPromise = await fp('name', 'nowPlaying.py') //search for any process with "nowPlaying.py in the name and assign to variable"
        .then(value => {return value})
    return pidPromise; 
}

const parseFindPythonPID = async () => {
    let npProcess = await findPythonPID().then(process => {return ({
        'running': Object.keys(process).length === 0, //if the promise returned by findPythonPID is empty,theres no process running
        'info': process[0]
    })})
    if (npProcess['running'] === true ){ 
        const pyScript = new PythonShell(np_script) 
    } 
    return npProcess['info']['pid']
}

parseFindPythonPID().then((val) => {pid = val})

if (Object.keys(data).length > 1) {
    console.log(`${data['Track Title']} | ${data['Artist']} | Sessions: ${data['Sessions']}`)
} else {
    console.log(' ')
}