@echo Off 
title DDS Conversion Script
cls

:: check nvdxt.exe
if not exist nvdxt.exe goto WARNING1

:: check tga
if not exist *.tga goto WARNING2

nvdxt -dxt5 -Cubic -quality_highest -file *.tga
echo.
echo Done!
goto END

:WARNING1
echo Copy the utility nvdxt.exe to the current folder!
goto END

:WARNING2
echo TGA not found
goto END

:END
pause
