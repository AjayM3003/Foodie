@echo off
echo ========================================
echo 🍔 Starting FoodieBot Application
echo ========================================
echo.
echo 📱 Web Interface: http://localhost:8501
echo 🌐 Opening in your default browser...
echo.
echo To stop the application:
echo   - Press Ctrl+C in this window
echo   - Or close this window
echo.
echo ========================================
echo.

python -m streamlit run enhanced_streamlit_app.py --browser.gatherUsageStats false

pause
