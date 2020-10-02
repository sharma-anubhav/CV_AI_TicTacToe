# CV_AI_TicTacToe

<h3>Libraries Required</h3>
1.Numpy<br>
2.opencv-python
<br>
Playing TicTacToe is fun, but whats more fun is playing it with computer on the wall begind you by simply pointing your finger.<br>
This is a Computer Vision and Artificial Intelligence bases game of tic tac toe.<br>
** made entirely from scratch without using any detection API.
<br>
We begin by taking the webcam feed and process each frame and process each frame and display a grid on it. The a 5 seconds time wndow is given for the user to point to a block where he wishes to make a move.At the end of 5 seconds we extract the grid block images and process them to extract contours.As the wall behind is plain. The only image with contours (starting from position 1) will be with the one with the finger.In order to get the contours right, we have to set a threshold range so that the lighting conditions dont give undesired contours.It uses minimax algorith to simulate the optimal moves of computer. 
<br>The game follows the standard rules of X/O.A grid will appear and you will have to point to where you want to place your mark.For this you get around 4 seconds of time.
<h3>**MAKE SURE THE BACKGROUND NEEDS TO BE LIKE A PLAIN WALL.

 
