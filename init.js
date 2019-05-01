let fileList = ['nodeList.json', 'linkList.json'];

function loadJSON(fileName, callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', fileName, false); // synchronous loading
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(JSON.parse(xobj.responseText));
        }
    };
    xobj.send(null);
}

let extractedArrays = [];

fileList.forEach(element => {
    loadJSON(element, function(json) {
        console.log(`${element} has been loaded.`); // this will log out the json object
        extractedArrays.push(json);
    
    });
});

console.log(extractedArrays);