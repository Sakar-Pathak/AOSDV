@ECHO OFF
::This is a simple batch file that runs the AOSDV
TITLE AOSDV
ECHO Running Advanced Orientation Simulator and Data Visualizer...........
start notepad "config\config.txt"
call "aosdv-venv\Scripts\activate.bat"
python "main.py"
PAUSE