@echo off
REM 🚀 Deployment Script - 13-Week Cash Flow Forecast
REM Tento skript pushne aplikáciu na GitHub a deployuje na Streamlit Cloud
REM Pre Windows
 
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  13-Week Cash Flow Forecast - Deployment Script   ║
echo ╚════════════════════════════════════════════════════╝
echo.
 
REM 1. Overenie Git
echo 📋 Overovanie...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git nie je nainštalovaný. Nainštalujte z: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git nájdený
 
REM 2. Navigácia do zložky
echo.
echo 📁 Navigácia do cf-forecast...
cd cf-forecast
if errorlevel 1 (
    echo ❌ Zložka 'cf-forecast' nenájdená!
    echo Vytvorte ju a skopírujte súbory.
    pause
    exit /b 1
)
 
REM 3. Git status
echo.
echo 📊 Git status:
git status
 
REM 4. Git push
echo.
echo 🚀 Pushuje sa do GitHub...
git push -u origin main
 
if errorlevel 0 (
    echo.
    echo ✅ Úspešne pushnuté na GitHub!
    echo.
    echo ╔════════════════════════════════════════════════════╗
    echo ║  🎉 Ďalší krok: Deploy na Streamlit Cloud        ║
    echo ╚════════════════════════════════════════════════════╝
    echo.
    echo 1. Choďte na https://streamlit.io/cloud
    echo 2. Prihlásite sa s GitHub účtom (tnagy421)
    echo 3. Kliknite 'New app'
    echo 4. Vyberte repo: tnagy421/cf-forecast
    echo 5. Vyberte branch: main
    echo 6. Nastavte main file path: app.py
    echo 7. Kliknite 'Deploy'
    echo.
    echo Vaša aplikácia bude dostupná na:
    echo https://cf-forecast-XXXXX.streamlit.app
) else (
    echo ❌ Push zlyhal. Skontrolujte:
    echo   - GitHub token je platný
    echo   - Internet pripojenie
    echo   - Git je nakonfigurovaný
)
 
pause
 