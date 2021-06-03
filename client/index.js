var express = require('express'); 
var bodyParser = require('body-parser'); 
var request = require('request-promise');
var path = require('path');
 
var app = express(); 
  
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname + '/public')));

app.get('/', function(req, res) {
   	res.render('index.html');
	res.end();
});
app.post('/question', async function (req, res) { 
    var data = req.body
    console.log(data)
    var options = { 
        method: 'POST', 
        uri: 'http://localhost:8080/answering_question', 
        body: data, 
        json: true // Automatically stringifies the body to JSON 
    }; 
     
    var returndata; 
    var sendrequest = await request(options) 
    .then(function (parsedBody) { 
        console.log(parsedBody); // parsedBody contains the data sent back from the Flask server 
        returndata = parsedBody; // do something with this data, here I'm assigning it to a variable. 
    }) 
    .catch(function (err) { 
        console.log(err); 
    }); 
     
    res.send(returndata); 
}); 
  
app.listen(3000, ()=>{
	console.log("http://localhost:3000");
}); 