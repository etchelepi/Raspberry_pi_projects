Server Client Side by Side 

This is a simple Python script that tests the picamera library's ability to view the motion vector data from the h.264 encoder. 

This is part of an attempt to create a stereo vision setup. Due to the limitations of the Pi only being able to have a single camera connected. The setup requires two Pi's connected together on a local network. 

One Pi Acts as the Server. The other a Client. 

The Server has two threads. One to capture images and convert them into a smaller image based on the vector data. The second to simply connect the client, receive data, and display both cameras. 

The Client starts the pi camera, and then tries to connect to the server. Once connected, it simply converts the vector data into an image, and sends it to the server to be viewed. 
 
 
 
