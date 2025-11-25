@echo off
REM Load Testing Script for API Monitoring System (Windows)
REM Generates traffic to test metrics collection and visualization

setlocal enabledelayedexpansion

set API_URL=http://localhost:8000
set DURATION=60
set CONCURRENT=5

if not "%1"=="" set DURATION=%1
if not "%2"=="" set CONCURRENT=%2

echo.
echo ========================================
echo   API Monitoring System - Load Test
echo ========================================
echo.
echo Duration: %DURATION% seconds
echo Concurrent requests: %CONCURRENT%
echo Target: %API_URL%
echo.
echo Starting load test...
echo.

setlocal enabledelayedexpansion
set /a end_time=%DURATION%

for /L %%i in (1,1,%DURATION%) do (
    echo [%%i/%DURATION%] Sending requests...
    
    REM Create users
    for /L %%j in (1,1,%CONCURRENT%) do (
        start /B curl -s -X POST "%API_URL%/api/users?name=User!RANDOM!&email=user!RANDOM!@example.com" >nul 2>&1
    )
    
    REM List users
    for /L %%j in (1,1,%CONCURRENT%) do (
        start /B curl -s "%API_URL%/api/users" >nul 2>&1
    )
    
    REM Get random users
    for /L %%j in (1,1,%CONCURRENT%) do (
        set /a user_id=!RANDOM! %% 10 + 1
        start /B curl -s "%API_URL%/api/users/!user_id!" >nul 2>&1
    )
    
    REM Slow endpoint
    for /L %%j in (1,1,%CONCURRENT%) do (
        start /B curl -s "%API_URL%/api/slow" >nul 2>&1
    )
    
    REM Error endpoint
    for /L %%j in (1,1,%CONCURRENT%) do (
        start /B curl -s "%API_URL%/api/error" >nul 2>&1
    )
    
    REM Health check
    for /L %%j in (1,1,%CONCURRENT%) do (
        start /B curl -s "%API_URL%/health" >nul 2>&1
    )
    
    timeout /t 1 /nobreak >nul
)

echo.
echo ========================================
echo   Load Test Completed!
echo ========================================
echo.
echo View metrics:
echo   - Prometheus: http://localhost:9090
echo   - Grafana: http://localhost:3000 (admin/admin)
echo   - Raw metrics: curl http://localhost:8000/metrics
echo.
pause
