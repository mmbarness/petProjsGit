const filePath = "<absolute path to json file goes here>"
const data = require(filePath)
console.log(`${data['Track Title']}, ${data['Artist']} | Sessions: ${data['Sessions']}`)