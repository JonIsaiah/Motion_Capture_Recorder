import pygame
import sys
import math
from time import sleep
import serial
from pygame.locals import *
import os
from datetime import datetime

opensim_model_mot_header = "Gait2354_mot_header.txt"		#header portion of .mot file for chosen body 
output_filename = "OutputFile.mot"					#name we want to give the output file
port = "COM7"


time = 0.00000000				#Define Variables for all of the angles in the gaitbody model file
pelvis_tilt = 0.00000000
pelvis_list = 0.00000000
pelvis_rotation = 0.00000000
pelvis_tx = 0.00000000
pelvis_ty = 0.00000000
pelvis_tz = 0.00000000
hip_flexion_r = 0.00000000
hip_adduction_r = 0.00000000
hip_rotation_r = 0.00000000
knee_angle_r = 0.00000000
ankle_angle_r = 0.00000000
subtalar_angle_r = 0.00000000
mtp_angle_r = 0.00000000
hip_flexion_l = 0.00000000
hip_adduction_l = 0.00000000
hip_rotation_l = 0.00000000
knee_angle_l = 0.00000000
ankle_angle_l = 0.00000000
subtalar_angle_l = 0.00000000
mtp_angle_l = 0.00000000
lumbar_extension = 0.00000000
lumbar_bending = 0.00000000
lumbar_rotation = 0.00000000
num_of_entries = 0;



pygame.init()

screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('ASU Human Machine Integration Laboratory Motion Recorder')


running = 1
state = 0	#0 for idle visualization, 1 for recording data

print("activating serial")
ser = serial.Serial(port, 115200, timeout=0)
print("serial active")

length1 = 150						#length of stick limb segments for animation
length2 = 175
length3 = 50

thighTilt = 0						# GEOMETRIC angles recorded by sensors
thighList = 0
shinTilt = -10
shinList = 0
ankleTilt = 0.00
ankleList = 0.00

hipFlexion = 0.00					# OPENSIM angles to be calculated
hipAdduction = 0.00
kneeAngle = 0.00
ankleAngle = 0.00

pitch1delta = 0.2
pitch2delta = 0.3

hipX=300							#initial positions for joint animation
hipY=100
kneeX=hipX
kneeY=hipY + length1
ankleX = hipX
ankleY = hipY + length2
toeX = hipX+length3
toeY = ankleY

font = pygame.font.Font(None, 26)	#font to be used


startTime = datetime.now()			#timer variables 
currentTime = datetime.now()






while running:	
	if state == 0:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				running = 0
			if event.type == pygame.MOUSEBUTTONUP:
				clickPos = pygame.mouse.get_pos()
				if clickPos[0] > 510 and clickPos[0] < 590:
					if clickPos[1] > 45 and clickPos[1] < 125:		#if record button clicked
						if state == 0:
							state = 1									#chaange the program state 
							os.remove("tempFile.txt")		#remove the temporary data file
							startTime = datetime.now()
							num_of_entries = 0
						else:
							state = 0
		
		
		
		
		data = ser.read(9999)
		if len(data) > 0:

			startPos = data.find("12")#finds the first occurance, really want to find last, fix later
			if startPos != -1:
				data = data[startPos:].split(",")	
				if data[0] == "12" and len(data) > 6 and data[6].find("\n") != -1:
					data[6] = data[6][:data[6].find("\n")]
				
					thighTilt = float(data[1])
					thighList = float(data[2])
					shinTilt = float(data[3])
					shinList = float(data[4])
					ankleList = float(data[5])
					ankleTilt = float(data[6]) - 30
					currentTime = datetime.now()
					
					

					#text = font.render("Hello, World", True, (0, 128, 0))
	
		screen.fill((0,0,0))
	
		#screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
	
	
		#calculate the coordinates to draw preview diagram
		
		time = (currentTime - startTime).total_seconds()
		text = font.render("Time: %.3f" % time, 1, (100, 100, 100))
		
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx + 340
		textpos.centery = 24
		screen.blit(text, textpos)		
		
		angleNames = ["GEOMETRIC ANGLES", "Thigh Tilt: %.3f" % (thighTilt), "Thigh List: %.3f" % (thighList), "Shin Tilt:  %.3f" % (shinTilt), "Shin List: %.3f" % (shinList), "Ankle Tilt: %.3f" % (ankleTilt), "Ankle List: %.3f" % (ankleList)]
		for x in range (0,7):
			text = font.render(angleNames[x], 1, (100, 100, 100))
		
			textpos = text.get_rect()
			textpos.centerx = screen.get_rect().centerx + 340
			textpos.centery = x*24 + 75
			screen.blit(text, textpos)		

		hipFlexion = thighTilt
		hipAdduction = thighList
		kneeAngle = shinTilt - thighTilt
		ankleAngle = -ankleTilt - shinTilt
			
		opensimNames = ["Opensim ANGLES", "Hip Flexion: %.3f" % (hipFlexion), "Hip Adduction: %.3f" % (hipAdduction), "Knee Angle:  %.3f" % (kneeAngle), "Ankle Angle: %.3f" % (ankleAngle)]
		for x in range (0,5):
			text = font.render(opensimNames[x], 1, (100, 100, 100))
		
			textpos = text.get_rect()
			textpos.centerx = screen.get_rect().centerx + 340
			textpos.centery = x*24 + 415
			screen.blit(text, textpos)
			
			
		#calculate the coordinates to draw preview diagram
		kneeY = hipY + int(math.cos(math.radians(thighTilt))*length1)
		kneeX = hipX + int(math.sin(math.radians(thighTilt))*length1)
		pygame.draw.line(screen, (100, 230,10), (hipX,hipY), (kneeX,kneeY), 3)
	
		ankleY = kneeY + int(math.cos(math.radians(shinTilt))*length2)
		ankleX = kneeX + int(math.sin(math.radians(shinTilt))*length2)
		pygame.draw.line(screen, (100, 230,10), (kneeX,kneeY), (ankleX,ankleY), 3)
	
		toeY = ankleY - int(math.sin(math.radians(-ankleTilt))*length3)
		toeX = ankleX + int(math.cos(math.radians(-ankleTilt))*length3)
		pygame.draw.line(screen, (100, 230,10), (ankleX,ankleY), (toeX,toeY), 3)	
		
		
		#draw the recording symbol
		pygame.draw.circle(screen, (175,0,15), (550,85), 40, 40)
		text = font.render("Start Recording", 1, (100, 100, 100))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx + 50
		textpos.centery = 140
		screen.blit(text, textpos)
	
		pygame.display.flip()		#display the frame
		sleep(.01)					#small delay to smoothe framerate
	
	
	
	
	
	
	else:
		with open("tempFile.txt", "w") as data_file:		#collect all data within this statement, write the data file
			while state == 1:							#Dont loop out of the with statement before the Record Button is pressed
			
				events = pygame.event.get()
				for event in events:
					if event.type == pygame.QUIT:
						running = 0
					if event.type == pygame.MOUSEBUTTONUP:
						clickPos = pygame.mouse.get_pos()
						if clickPos[0] > 510 and clickPos[0] < 590:
							if clickPos[1] > 45 and clickPos[1] < 125:		#See if Record Button was clicked
								if state == 0:								#If so change the state 
									state = 1
									startTime = datetime.now()
									num_of_entries = 0
								else:
									state = 0
									
									with open(output_filename, "w") as motion_file:

										with open(opensim_model_mot_header) as headerFile:		#read the the header file
											header = headerFile.readlines()
											header[2] = "nRows="+str(num_of_entries)+"\n"  	#edit the number of rows to match the actual number of rows
										
										for line in header:
											motion_file.write(line)		#write the edited header to the beginning of the output file

										motion_file.write("\n")	#add newline between files to keep formatting good	
										
										with open("tempFile.txt") as dataFile:		#read the data file and copy data to output file
											for line in dataFile:
												motion_file.write(line)

												
									#os.remove("tempFile.txt")		#remove the temporary data file  have to move this elsewhere
									
									
									
									startTime = datetime.now()
									
				data = ser.read(9999)
				if len(data) > 0:

					startPos = data.find("12")#finds the first occurance, really want to find last, fix later
					if startPos != -1:
						data = data[startPos:].split(",")	
						if data[0] == "12" and len(data) > 6 and data[6].find("\n") != -1:
							data[6] = data[6][:data[6].find("\n")]
					
							thighTilt = float(data[1])
							thighList = float(data[2])
							shinTilt = float(data[3])
							shinList = float(data[4])
							ankleList = float(data[5])
							ankleTilt = float(data[6]) - 30
							currentTime = datetime.now()
						
						

							#text = font.render("Hello, World", True, (0, 128, 0))
		
				screen.fill((0,0,0))
		
				#screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
		
		
				#calculate the coordinates to draw preview diagram
			
				time = (currentTime - startTime).total_seconds()
				text = font.render("Time: %.3f" % time, 1, (100, 100, 100))
			
				textpos = text.get_rect()
				textpos.centerx = screen.get_rect().centerx + 340
				textpos.centery = 24
				screen.blit(text, textpos)		
				
				#Print Geometric Angles
				angleNames = ["GEOMETRIC ANGLES", "Thigh Tilt: %.3f" % (thighTilt), "Thigh List: %.3f" % (thighList), "Shin Tilt:  %.3f" % (shinTilt), "Shin List: %.3f" % (shinList), "Ankle Tilt: %.3f" % (ankleTilt), "Ankle List: %.3f" % (ankleList)]
				for x in range (0,7):
					text = font.render(angleNames[x], 1, (100, 100, 100))
			
					textpos = text.get_rect()
					textpos.centerx = screen.get_rect().centerx + 340
					textpos.centery = x*24 + 75
					screen.blit(text, textpos)		

				hipFlexion = thighTilt
				hipAdduction = thighList
				kneeAngle = shinTilt - thighTilt
				ankleAngle = -ankleTilt - shinTilt
				
				#Print Opensim Angles
				opensimNames = ["Opensim ANGLES", "Hip Flexion: %.3f" % (hipFlexion), "Hip Adduction: %.3f" % (hipAdduction), "Knee Angle:  %.3f" % (kneeAngle), "Ankle Angle: %.3f" % (ankleAngle)]
				for x in range (0,5):
					text = font.render(opensimNames[x], 1, (100, 100, 100))
			
					textpos = text.get_rect()
					textpos.centerx = screen.get_rect().centerx + 340
					textpos.centery = x*24 + 415
					screen.blit(text, textpos)
				
				
				#calculate the coordinates to draw preview diagram
				kneeY = hipY + int(math.cos(math.radians(thighTilt))*length1)
				kneeX = hipX + int(math.sin(math.radians(thighTilt))*length1)
				pygame.draw.line(screen, (100, 230,10), (hipX,hipY), (kneeX,kneeY), 3)
		
				ankleY = kneeY + int(math.cos(math.radians(shinTilt))*length2)
				ankleX = kneeX + int(math.sin(math.radians(shinTilt))*length2)
				pygame.draw.line(screen, (100, 230,10), (kneeX,kneeY), (ankleX,ankleY), 3)
		
				toeY = ankleY - int(math.sin(math.radians(-ankleTilt))*length3)
				toeX = ankleX + int(math.cos(math.radians(-ankleTilt))*length3)
				pygame.draw.line(screen, (100, 230,10), (ankleX,ankleY), (toeX,toeY), 3)	
			
			
				#draw the recording symbol
				pygame.draw.circle(screen, (175,0,15), (550,85), 40, 40)
				text = font.render("Stop Recording", 1, (100, 100, 100))
				textpos = text.get_rect()
				textpos.centerx = screen.get_rect().centerx + 50
				textpos.centery = 140
				screen.blit(text, textpos)
		
				pygame.display.flip()		#display the frame
				
				
				#finally write the line of data to the file
				hip_flexion_r = hipFlexion
				hip_adduction_r = hipAdduction
				knee_angle_r = kneeAngle
				ankle_angle_r = ankleAngle
				data_file.write("      %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f	        %.8f\n" % (time, pelvis_tilt,pelvis_list,pelvis_rotation, pelvis_tx, pelvis_ty, pelvis_tz, hip_flexion_r, hip_adduction_r, hip_rotation_r, knee_angle_r, ankle_angle_r, subtalar_angle_r, mtp_angle_r, hip_flexion_l, hip_adduction_l, hip_rotation_l, knee_angle_l, ankle_angle_l, subtalar_angle_l, mtp_angle_l, lumbar_extension, lumbar_bending, lumbar_rotation))
				num_of_entries = num_of_entries+1 #file header needs to know how many rows of data we have
				sleep(.01)					#small delay to smoothe framerate

		
