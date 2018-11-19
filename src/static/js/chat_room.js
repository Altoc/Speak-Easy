$(document).ready(function () {
	var socket = io.connect('https://' + document.domain + ":" + location.port);

	var defaultRadius = 10000;
	
	var receivingMsgSwitcher = 0; //switches message receiving function in order to assign user-specific color
	var amtOfColors = 15;
	var myColor = colorPicker(Math.floor(Math.random() * Math.floor(9)));

   function colorPicker(x){
	   switch(x){
		   case "0": return "Aqua"; break;
		   case "1": return "Beige"; break;
		   case "2": return "Brown"; break;
		   case "3": return "Coral"; break;
		   case "4": return "Crimson"; break;
		   case "5": return "DarkMagenta"; break;
		   case "6": return "DarkSlateGray"; break;
		   case "7": return "DimGray"; break;
		   case "8": return "ForestGreen"; break;
		   case "9": return "Gold"; break;
		   case "a": return "Aqua"; break;
		   case "b": return "Beige"; break;
		   case "c": return "Brown"; break;
		   case "d": return "Coral"; break;
		   case "e": return "Crimson"; break;
	   }
   }
   
   //TODO: set user-color to the same as others see
   function sendFromTextBox() {
      chat = document.getElementById("msg_list");
      msg = document.createElement('p');
      msg.innerHTML = document.getElementById("post").value;
      chat.appendChild(msg);
      socket.send(document.getElementById("post").value);
      document.getElementById("post").value = "";
	  msg.style.clear = "both";
	  msg.style = "text-align:right;";
	  msg.style.fontFamily = "Limelight";
	  //msg.style.color = myColor;
	  chat.scrollTop = chat.scrollHeight;
   }

   
   // TODO: should become sendPosition and sendRadius later
   function sendData(lat, lon, radius) {
      socket.emit('location', {
         'lat': lat,
         'lon': lon,
         'radius': radius
      });
   }

   $("#submit_post_btn").click(function () {
      sendFromTextBox();
   });

   $("#post").on('keydown', function(event) {
      if(event.key == "Enter") {
         event.preventDefault();

         sendFromTextBox();
      }
   });

   $("#send_location").click(function () {
      navigator.geolocation.getCurrentPosition(function(position) { 
         sendData(position.coords.latitude, position.coords.longitude, defaultRadius);
      });
   });

   socket.on('connect', function() {
      navigator.geolocation.getCurrentPosition(function(position) { 
         sendData(position.coords.latitude, position.coords.longitude, defaultRadius);
      });
   });
   
   socket.on('updateUsers', function(param) {
		users = document.getElementById("user_count");
		users.innerHTML = param;
   });
   
   socket.on('message', function(msg) {
	if(receivingMsgSwitcher == 0){
		chat = document.getElementById("msg_list");
		displayedMessage = document.createElement('p');
		displayedMessage.innerHTML = msg;
		chat.appendChild(displayedMessage);
		chat.scrollTop = chat.scrollHeight;
		displayedMessage.style.fontFamily = "Limelight";
		
		receivingMsgSwitcher = receivingMsgSwitcher + 1;
	}
	else if(receivingMsgSwitcher == 1){
		displayedMessage.style.color = colorPicker(msg);
		
		receivingMsgSwitcher = receivingMsgSwitcher - 1;
	}
   });

   $(window).on('beforeunload',function(){
      socket.disconnect();
   });
});