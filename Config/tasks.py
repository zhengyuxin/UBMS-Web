import os
import sys
import time

from celery import Celery
from Config.PlatformPdo2 import PlatformPdo2

sys.path.append(r'C:\Users\yzhen22\workspace\OC\Tools\SdbTools')
from Config.PlatformPdo2 import PlatformPdo2

_platformpdo2_obj = None

@app.task
def preload_repository(bim_path):
	global _platformpdo2_obj
	if not _platformpdo2_obj:
		start_time = time.time()  
		_platformpdo2_obj = PlatformPdo2()
		if _platformpdo2_obj.OpenProject(bim_path):
			return 'PID:%s, success to pre-open project %s, time:%s' % (os.getpid(), bim_path, time.time()-start_time)
		else:
			return 'PID:%s, fail to pre-open project %s, time:%s' % (os.getpid(), bim_path, time.time()-start_time)

	else:
		pass

@app.task
def open(bim_path):
	global _platformpdo2_obj
	start_time = time.time()  
	if _platformpdo2_obj.OpenProject(bim_path):
		return 'PID:%s, success to open project %s, time:%s' % (os.getpid(), bim_path, time.time()-start_time)
	else:
		return 'PID:%s, fail to open project %s, time:%s' % (os.getpid(), bim_path, time.time()-start_time)


@app.task
def get()