var fs = require('fs')

fs.writeFileSync('lib/transfermarkt.py',
  JSON.parse(fs.readFileSync("notebooks/transfermarkt.ipynb"))['cells'][0]['source'].join('') + '\n')
