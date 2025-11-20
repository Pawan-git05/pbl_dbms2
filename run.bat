@echo off
echo ResQTrack - Animal Rescue Coordination Platform
echo ==============================================
echo.
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Starting the application...
echo Open your browser and go to http://localhost:5000
python app.py
pause