echo off
set path=%path%; C:\Users\yzhen22\AppData\Local\Continuum\Anaconda\Scripts
echo=================================================================================
echo celery -A tasks worker --loglevel=info -c 1 -n w1@%%h
echo.
echo use flower to check status
echo.
echo --without-gossip      Do not subscribe to other workers events.
echo --without-mingle      Do not synchronize with other workers at startup.
echo.
echo --broker_api=http://127.0.0.1:15672/api/
echo.
echo=================================================================================
:begin
set/p Worker_No=please input the worker No:
cd %~dp0\..
celery -A ConfigWeb worker --loglevel=info -c 1 -n w"%Worker_No%"@%%h
:next
cmd