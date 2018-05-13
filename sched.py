"""Schedule bot's jobs"""

import schedule
import time
from frontier import main as frontier_job
from replies import main as replies_job
from tip import main as tip_job


schedule.every(10).seconds.do(frontier_job)
schedule.every(10).seconds.do(replies_job)
schedule.every(10).seconds.do(tip_job)

while 1:
    schedule.run_pending()
    time.sleep(1)