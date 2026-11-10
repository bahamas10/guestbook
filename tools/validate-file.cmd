@echo off
setlocal

:check-perl
perl -v > nul 2> nul
if %errorlevel%==0 goto run-validate-file
echo Whoops! Can not find "perl" executable.
echo To use "validate-file" you need to install Perl.
echo Be sure that your local PATH variable contains
echo the path to Perl executable.
goto end

:run-validate-file
set script_name=%0
if %script_name:~-4,1%==. set script_name=%script_name:~0,-4%
perl %script_name% %1

:end
endlocal