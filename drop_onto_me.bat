@echo off 
goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Seems like Python not installed in your Windows system.
echo Install it from https://www.python.org/downloads/windows/
echo If you are shure the Python installed, add it's path to the system global PATH environment variable.
echo See here how to do it: https://geek-university.com/add-python-to-the-windows-path/
goto :EOF

:PYTHON_DOES_EXIST
cd /d "%~dp0"

:: Prefer output in JSON and HTML with overwriting
python jsonlz4_to_html.py -o -j -t "%~f1"

:: Uncomment underlying line to prefer output in HTML format
:: python jsonlz4_to_html.py -t "%~f1"

:: Uncomment underlying line to prefer output in JSON format
:: python jsonlz4_to_html.py -j "%~f1"

:: Uncomment underlying line to prefer output in JSON and HTML with zero output with overwriting
:: python jsonlz4_to_html.py -o -j -t -s "%~f1"

goto :EOF

