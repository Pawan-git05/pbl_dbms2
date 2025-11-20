Write-Host "ResQTrack - Animal Rescue Coordination Platform" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host ""
Write-Host "Starting the application..." -ForegroundColor Yellow
Write-Host "Open your browser and go to http://localhost:5000" -ForegroundColor Cyan
python app.py