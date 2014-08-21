import os
import sys
import time

from celery import Celery

sys.path.append(r'C:\Users\yzhen22\workspace\OC\Tools\SdbTools')
from Config.PlatformPdo2 import PlatformPdo2
BIM_PATH = r'C:\Users\yzhen22\Intel\Unified Binary Management Suite\Test\Test.bim'

app = Celery('tasks', broker='amqp://guest@localhost//')
app.config_from_object('celeryconfig')

_platformpdo2_obj = None

@app.task
def open():
	global _platformpdo2_obj
	start_time = time.time()  
	if _platformpdo2_obj.OpenProject(BIM_PATH):
		return 'PID:%s, success to open project %s, time:%s' % (os.getpid(), BIM_PATH, time.time()-start_time)
	else:
		return 'PID:%s, fail to open project %s, time:%s' % (os.getpid(), BIM_PATH, time.time()-start_time)

@app.task
def preload_repository():
	global _platformpdo2_obj
	if not _platformpdo2_obj:
		start_time = time.time()  
		_platformpdo2_obj = PlatformPdo2()
		if _platformpdo2_obj.OpenProject(BIM_PATH):
			return 'PID:%s, success to pre-open project %s, time:%s' % (os.getpid(), BIM_PATH, time.time()-start_time)
		else:
			return 'PID:%s, fail to pre-open project %s, time:%s' % (os.getpid(), BIM_PATH, time.time()-start_time)

	else:
		pass

