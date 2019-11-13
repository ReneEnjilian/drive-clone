

var count = 0;
if (count == 0){
    console.log("first!!");
    fetch("http://127.0.0.1:4000/getdata")
        .then(response => response.json())
        .then(function(data){
            render_to_display(data)
        })
        .then(function(){count=1})
    
}


const submitButton = document.getElementById("submit");
const submittedFile = document.getElementById("file");

submitButton.addEventListener("click", function(){send(submittedFile)});


async function send(submittedFile){
    let file = submittedFile.files[0];
    let formData = new FormData();
    formData.append('file', file);
    let response = await fetch('http://127.0.0.1:4000/upload', {
        method: 'POST',
        body: formData
    })
    let result = await response.json();
    
    render_to_display(result);
    

}

function render_to_display(response){

   
    response.forEach(function(jsonObj){
        //console.log(response);
        let row = document.createElement('tr');
        let table = document.querySelector(".file_table");
        row.id = jsonObj["id"];

        
        let cell1 = document.createElement("td");
        cell1.textContent = jsonObj["filename"];
        row.appendChild(cell1);

        let cell2 = document.createElement("td");
        cell2.textContent = jsonObj["date"];
        row.appendChild(cell2);

        let cell3 = document.createElement("td");
        cell3.textContent = jsonObj["size"];
        row.appendChild(cell3);

        let cell4 = document.createElement("td");
        let delete_button = document.createElement("button");
        delete_button.addEventListener("click", function(){delete_row(jsonObj.id)});
        let i_tag_del = document.createElement("i");
        
        i_tag_del.className = "material-icons";
        i_tag_del.textContent = "delete"
        delete_button.appendChild(i_tag_del);
        //delete_button.textContent = "test";
        
        cell4.appendChild(delete_button);
        row.appendChild(cell4);

        let cell5 = document.createElement("td");
        let download_button = document.createElement("button");
        download_button.addEventListener("click", function(){download_file(jsonObj.id, cell1)});
        let i_tag_download = document.createElement("i");
        i_tag_download.className = "material-icons";
        i_tag_download.textContent = "cloud_download";
        download_button.appendChild(i_tag_download);
        cell5.appendChild(download_button);
        row.appendChild(cell5);

        let cell6 = document.createElement("td");
        let rename_button = document.createElement("button");
        rename_button.textContent = "chnage name";

        rename_button.addEventListener("click", function(){reanme_file(jsonObj.id)});
        cell6.appendChild(rename_button);
        
    
        row.appendChild(cell6);
        table.appendChild(row);
    });

}

async function delete_row(id){
    let url = "http://127.0.0.1:4000/delete/";
    let operation = id.toString();
    let delete_url = url + operation;
    //alert(delete_url);
    let response = await fetch(delete_url, {
        method: "DELETE"
    })

    let parsedData = await response.json();
    let success = parsedData.success;
    console.log(parsedData);
    if(success == false){
        alert("Sorry this file is not availiable anymore");
    }else{
    
        let current_row = document.getElementById(id);
        current_row.remove();
    }
    
}

async function download_file(id, cell1){
    let url = "http://127.0.0.1:4000/download/";
    let file_id = id.toString();
    let download_url = url + id;
    var win = window.open(download_url, '_blank');
}

async function reanme_file(id){
   
    /*var node = document.getElementById(id);
    var children = node.childNodes;
    console.log(children[0].textContent);*/
    let new_filename = prompt("Enter new filename:");
    new_filename = new_filename.trim();
    while(new_filename == ""){
        let new_filename2 = prompt("You have to enter a name, sry :)");
        new_filename = new_filename2.trim();
    }

    //console.log("hier");
    //console.log(new_filename);

     if(new_filename != ""){
         // neuen namen bauen --> ergänze extension 
         // schicke : url bauen, json bauen
         // json mit success = true/ false lesen
         // wenn true dann update cell1
         // wenn false dann Fehlermeldung --> "diese datei ist nicht mehr verfügbar"
         buildPackage(id, new_filename);

     }
}


async function buildPackage(id, new_filename){
    let row = document.getElementById(id);
    let cells_in_row = row.childNodes;
    let oldName = cells_in_row[0].textContent;
    let splitArray = oldName.split(".");
    let extension = splitArray[splitArray.length - 1];
    //console.log(new_filename);
    //console.log(oldName);
    //console.log(extension);
    let fullName = new_filename + "." + extension;
    //console.log(fullName);
    let idToSend = id.toString();
    let url = "http://127.0.0.1:4000/rename/" + idToSend;
    //console.log(url);

    let obj = {filename: fullName};
    let jsonObj = JSON.stringify(obj);
    fetch(url, {
        method: "POST",
        body: jsonObj,
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(function(response){
        handleResponse(response, id);
    })


    

}

function handleResponse(response, id){
    //let result = response.json();
    let success = response.success;
    if(success == false){
        alert("Sorry this file is not availiable anymore");
    }else{
        var row = document.getElementById(id);
        let cells_in_row = row.childNodes;
        let cell1 = cells_in_row[0];
        console.log(response.new_filename);
        cell1.textContent = response.new_filename;

    }

}