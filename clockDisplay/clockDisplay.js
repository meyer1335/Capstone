"use strict";

//import { readFile } from 'fs';

let theDate;
let alarmTime = "9:00";

function updateTime(initializing) {
    let d = new Date();
    let h = d.getHours();
    let m = d.getMinutes();
    if(m < 10) {    //Because single digit minutes come back without a leading zero
        m = "0" + m.toString();
    }
    let pm = 0;
    let ampms = ["AM","PM"];
    if(h > 12) {    //convert to 12 hour time and set am or pm
        pm = 1;
        h -=12;
    }
    document.getElementsByClassName("time")[0].innerHTML = h + ":" + m;
    document.getElementById("ampm").innerHTML = ampms[pm];
	document.getElementsByClassName("alarm")[0].innerHTML = "Alarm Time - " + alarmTime;
    
	//updateAlarmTime();

    if(initializing || theDate != d.getDate())  //on first time and on date change
        updateDayDate(d);
		
	
}

function updateDayDate(d) {
  
    let weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
       
    document.getElementsByClassName("weekday")[0].innerHTML = weekdays[d.getDay()];
    document.getElementsByClassName("date")[0].innerHTML = months[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
    //Update global variable theDate
    theDate = d.getDate();
    
}

/*
function updateAlarmTime() {
	let textfile = fs.readFile("alarm_time.txt");
	alarmTime = textfile.toString();
} */

//Call updateTime and let it know we're initializing
updateTime(1);
//Call updateTime every half-second. Could call every second, we're only displaying hours and minutes
let tick = setInterval(updateTime,500);