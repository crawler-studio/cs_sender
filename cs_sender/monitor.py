"""
@Description: 
@Usage: 
@Author: liuxianglong
@Date: 2022/5/14 上午11:52
"""
import logging
from .core import BaseInfo

logger = logging.getLogger(__name__)


class Monitor(BaseInfo):
    """Monitor error log rate"""

    def __init__(self, crawler, spider, *args, **kwargs):
        BaseInfo.__init__(self, crawler, spider)
        self.enable_monitor_rule = crawler.settings.getbool('CS_ENABLE_MONITOR_RULE', True)

    def spider_open(self, spider):
        if self.enable_monitor_rule:
            self.api.add_monitor_rule(self.host, self.project, self.spider, self.job_id)

    def spider_close(self, spider, reason):
        if self.enable_monitor_rule:
            self.api.del_monitor_rule(self.job_id)
