from kombu import Queue

BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp'

CELERY_IMPORTS = ("tasks")

# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True
CELERYD_CONCURRENCY = 3


CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

# This option enables so that every worker has a dedicated queue, 
# so that tasks can be routed to specific workers.
# The queue name for each worker is automatically generated based on 
# the worker hostname and a .dq suffix, using the C.dq exchange.
# For example the queue name for the worker with node name w1@example.com becomes:
# w1@example.com.dq
# Then you can route the task to the task by specifying the hostname 
# as the routing key and the C.dq exchange:
# IMPORTANT the wildcard characters: 
# * (matches a single word), and # (matches zero or more words).
CELERY_WORKER_DIRECT = True