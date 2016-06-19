# Motion_Capture_Recorder
Motion capture recorder tool developed for use with the wearable wireless sensor network for exoskeleton motion capture.  Developed for the ASU Human-Machine Integration Laboratory.

This tool replaces the old method of manually converting data files.

To Dos:
  Add dialog box for com port selection
  3d visualization ?  would require moving to different gfx package

To use the tool:
  1. Connect to central data receiver via serial > usb 
  2. open device manager and note COM port
  3. edit top of MotionRecorder.py to reflect the correct COM port
  4. ensure that the header file from your chosen sim-body .mot file is present in the same folder
  5. Open the motion recorder app (python MotionRecorder.py)
  6. You may need to remove your usb and re-plug to facilitate connection to data stream
  7. Press the Start Recording button to begin recording data
  8. When ready, Press the Stop Recording button to stop recording data
  9. The motion data will be converted automatically into opensim .mot format and will appear in the directory, the file will be named OutputFile.mot, rename the file to something descriptive
