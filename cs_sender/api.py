"""
@Description: 
@Usage: 
@Author: liuxianglong
@Date: 2022/5/13 上午1:11
"""
import logging
import requests

logger = logging.getLogger(__name__)


def cs_api(func):

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.warning(f'API error, {e}, funciton: {func.__name__}, args: {args}, kwargs: {kwargs}')

    return wrapper


class API(object):

    def __init__(self, settings):
        self._settings = settings
        self._host = settings.get('CS_BACKEND', 'http://localhost:16800')
        self._spider_stats_end_point = f"{self._host}/api/v1/scrapyd/spiderStats/"
        self._errlog_rate_end_point = f"{self._host}/api/v1/logs/errorLogRate/"
        self._errlog_content_end_point = f"{self._host}/api/v1/logs/errorLogContent/"
        self._monitor_rule_end_point = f'{self._host}/api/v1/schedule/monitorRules/'
        self._api_token = settings.get('CS_API_TOKEN', '')

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self._api_token}'
        }

    @cs_api
    def send_stats_data(self, raw_json):
        response = requests.post(self._spider_stats_end_point, headers=self.headers, json=raw_json)
        logger.info(f'Send scrapy stats success, {response.text}')

    @cs_api
    def send_errlog_rate(self, raw_json):
        response = requests.post(self._errlog_rate_end_point, headers=self.headers, json=raw_json)
        logger.info(f'Send errlog rate success, {response.text}')

    @cs_api
    def send_errlog_content(self, raw_json):
        response = requests.post(self._errlog_content_end_point, headers=self.headers, json=raw_json)
        logger.info(f'Send errlog content success, {response.text}')

    @cs_api
    def add_monitor_rule(self, host, project, spider, jobid):
        d = {
            "spider_host": host,
            "spider_project": project,
            "spider_name": spider,
            "spider_job_id": jobid,
            "monitor_freq": self._settings.get('CS_MONITOR_FREQ', 300),
            "errlog_rate_limit": self._settings.get('CS_ERRLOG_RATE_LIMIT', 0.005),
            "memory_use_limit": self._settings.get('CS_MEMORY_USE_LIMIT', 500)
        }
        response = requests.post(self._monitor_rule_end_point, headers=self.headers, json=d)
        logger.info(f'Add monitor rule, {response.text}')

    @cs_api
    def del_monitor_rule(self, jobid):
        d = {
            "spider_job_id": jobid,
        }
        response = requests.delete(self._monitor_rule_end_point, headers=self.headers, json=d)
        logger.info(f'Delete monitor rule, {response.text}')
