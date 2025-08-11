var socket = io.connect('http://127.0.0.1:5000');

document.getElementsByName("valve").forEach(element => {
    element.addEventListener("click", valveStatusChanged);
}); 


function valveStatusChanged(){   
    if(this.checked){
        message = this.id+"1";
    }
    else{
        message = this.id+"0";
    }
    socket.emit('change', message);
}

function updateValveStatus(data){
    data = JSON.parse(data);
    console.log('Change: ', "gpio:", data.gpio, "status:", data.status);

    valve = document.getElementById("gpio-"+data.gpio);
    if(valve != null){
        if(data.status==1){
            valve.checked=true;
        }
        else if(data.status==0){
            valve.checked=false;
        }
    }
}

socket.on('connect', function() {
});

socket.on('statusChanged', function(data) {
    updateValveStatus(data);
});

socket.on('initialStatuses', function(data) {
    updateValveStatus(data);
});

socket.on('message', function(data) {
    console.log('Message content: ', data);
});