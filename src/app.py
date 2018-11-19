from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, send, emit
from coordinate import Coordinate
from userdata import UserData
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretytypeword!'
socketio = SocketIO(app)

connections = dict()
	
amtOfUsers = 0;

#Called when the server recieves a message from the client that is marked as a 'message' (chat)
@socketio.on('message')
def handleMessage(msg):
	global amtOfUsers;

	emit('updateUsers', amtOfUsers)
	
	print("Message: " + msg)
	print("Recieved message from: " + request.sid + ".\n")
	print("Color ID of sender: " + request.sid[:1])
	
	colorId = request.sid[:1]
	
	for key, value in connections.items():
		if(key != request.sid):
			if(value.position.distanceInMeters(connections[request.sid].position) < value.radius):
				send(msg, room=key)		#contains message
				send(colorId, room=key)	#contains color of user messages
   
#Called when the server recieves a message from the client that is marked as 'location'
@socketio.on('location')
def recievedLocation(data):
   global amtOfUsers;
   
   print("Recieved location data from: " + request.sid + ".\n")
   print("Latitude: " + str(data['lat']) + "\n")
   print("Longitude: " + str(data['lon']) + "\n")
   print("Radius: " + str(data['radius']) + "\n")
   
   amtOfUsers = amtOfUsers + 1
   print("Amount of Users Connected: " + str(amtOfUsers) + "\n")
   #emit('location', amtOfUsers)
   
   coord = Coordinate()
   coord.setLatitude(data['lat'])
   coord.setLongitude(data['lon'])

   userData = UserData()
   userData.setPosition(coord)
   userData.setRadius(data['radius'])
   
   connections[request.sid] = userData
   
#Called when a websocket connection is disconnected (that connection becomes unresponsive, for example if someone closes the browser window). 
@socketio.on('disconnect')
def userDisconnected():
   global amtOfUsers;

   print("UserID disconnected: " + request.sid + "\n")
   amtOfUsers = amtOfUsers - 1
   print("Amount of Users Connected: " + str(amtOfUsers) + "\n")
   
   connections.pop(request.sid, None)

#When a user opens up the webpage, send the html file along with the css and javascript. 
@app.route("/")
def index():
	return render_template("chat_room.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', ssl_context='adhoc') # , port=443) #app.run(Debug=True)
