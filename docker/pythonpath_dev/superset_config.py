# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache
from flask_appbuilder.security.manager import AUTH_OAUTH
from custom_sso_security_manager import CustomSsoSecurityManager

logger = logging.getLogger()

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = (
    f"{DATABASE_DIALECT}://"
    f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
    f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG


class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = ("superset.sql_lab",)
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False

# CSRF
SECRET_KEY = os.getenv('SUPERSET_SECRET_KEY')
# Flask-WTF flag for CSRF
ENABLE_PROXY_FIX= True
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True
TALISMAN_ENABLED = False
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# google oauth
AUTH_TYPE = AUTH_OAUTH

# 사용자 권한 초기 어드민 설정
AUTH_ROLE_PUBLIC = 'Admin'
AUTH_USER_REGISTRATION_ROLE = "Admin"
AUTH_USER_REGISTRATION = True

OAUTH_PROVIDERS = [{
        "name": "google",
        "whitelist": ["@algocarelab.com"],
        "token_key": "access_token",
        "icon": "fa-google", 
        "remote_app": {
            "api_base_url": "https://www.googleapis.com/oauth2/v2/",
            "client_kwargs": {
                    "scope": "email profile"
            },
            "access_token_url": "https://accounts.google.com/o/oauth2/token",
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
            "request_token_url": None,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET
        }
}]
# CUSTOM_SECURITY_MANAGER 사용시 코드 오류 발견, 일단 없어도 될듯 하여 주석 처리
# CUSTOM_SECURITY_MANAGER = CustomSsoSecurityManager
SQLLAB_CTAS_NO_LIMIT = True

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")


ROW_LIMIT = 5000
# For SQL LAB
SQL_MAX_ROW = 5000
WEBDRIVER_TYPE = "firefox"
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]

WEBDRIVER_BASEURL = "http://superset:8088/"
# The base URL for the email report hyperlinks.
# WEBDRIVER_BASEURL = "http://localhost:8088"
# This is the link sent to the recipient. Change to your domain, e.g. https://superset.mydomain.com
WEBDRIVER_BASEURL_USER_FRIENDLY = "https://superset.algocare.link"
SCREENSHOT_LOCATE_WAIT = 100
SCREENSHOT_LOAD_WAIT = 600

from superset.tasks.types import ExecutorType

THUMBNAIL_SELENIUM_USER = 'admin'
ALERT_REPORTS_EXECUTE_AS = [ExecutorType.SELENIUM]

SCHEDULED_QUERIES = {
    # This information is collected when the user clicks "Schedule query",
    # and saved into the `extra` field of saved queries.
    # See: https://github.com/mozilla-services/react-jsonschema-form
    'JSONSCHEMA': {
        'title': 'Schedule',
        'description': (
            'In order to schedule a query, you need to specify when it '
            'should start running, when it should stop running, and how '
            'often it should run. You can also optionally specify '
            'dependencies that should be met before the query is '
            'executed. Please read the documentation for best practices '
            'and more information on how to specify dependencies.'
        ),
        'type': 'object',
        'properties': {
            'output_table': {
                'type': 'string',
                'title': 'Output table name',
            },
            'start_date': {
                'type': 'string',
                'title': 'Start date',
                # date-time is parsed using the chrono library, see
                # https://www.npmjs.com/package/chrono-node#usage
                'format': 'date-time',
                'default': 'tomorrow at 9am',
            },
            'end_date': {
                'type': 'string',
                'title': 'End date',
                # date-time is parsed using the chrono library, see
                # https://www.npmjs.com/package/chrono-node#usage
                'format': 'date-time',
                'default': '9am in 30 days',
            },
            'schedule_interval': {
                'type': 'string',
                'title': 'Schedule interval',
            },
            'dependencies': {
                'type': 'array',
                'title': 'Dependencies',
                'items': {
                    'type': 'string',
                },
            },
        },
    },
    'UISCHEMA': {
        'schedule_interval': {
            'ui:placeholder': '@daily, @weekly, etc.',
        },
        'dependencies': {
            'ui:help': (
                'Check the documentation for the correct format when '
                'defining dependencies.'
            ),
        },
    },
    'VALIDATION': [
        # ensure that start_date <= end_date
        {
            'name': 'less_equal',
            'arguments': ['start_date', 'end_date'],
            'message': 'End date cannot be before start date',
            # this is where the error message is shown
            'container': 'end_date',
        },
    ]
    # link to the scheduler; this example links to an Airflow pipeline
    # that uses the query id and the output table as its name
    # 'linkback': (
    #     'https://airflow.example.com/admin/airflow/tree?'
    #     'dag_id=query_${id}_${extra_json.schedule_info.output_table}'
    # ),
}

