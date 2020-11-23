# -*- coding: utf-8 -*-
import os
from lms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/"
for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR


DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Disable django/drf deprecation warnings
import logging
import warnings
from django.utils.deprecation import RemovedInDjango30Warning, RemovedInDjango31Warning
from rest_framework import RemovedInDRF310Warning, RemovedInDRF311Warning
warnings.simplefilter('ignore', RemovedInDjango30Warning)
warnings.simplefilter('ignore', RemovedInDjango31Warning)
warnings.simplefilter('ignore', RemovedInDRF310Warning)
warnings.simplefilter('ignore', RemovedInDRF311Warning)

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://academia.aulanet.com.bo/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "IZjZwOS3NQX8EKAzATkFGrmJ"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "OfBo9zbU9YZf0AT-JVPNQrF2Cmnx3Ah7A-2BM90Mi61HF6p2kzdDsPTnANqYOh5LISabO0zPZdH8o2KmRcyISmoP7lYcnes8W_gR9wN-xPD28KiWCwYfw3v86ZVVdoUR8QNw-RpOSFgMewZtpHIwOBAhGcgUaRlMN8blZdgxcL6yXs2K0WzCTJmEJTQH08Sl5zXF4Q7Y-bps-3SUa99z60F3sw75otvQ7umQ3RXrqN4sOVq20Uvp51VeD2ECElcZAEqbBOvVgZGiJIfI9fcRLwoLoYy8j3HzMMfzokl3YPdVvc3ogATUeOVw_602g09nEytQqzhx722msPx1mefYhQ",
        "n": "mrLYkSLnjS8T21vW88_8-wcC2efbub_rxVQUZMtcXfK11EjtJSdgQyxB9E3g9V9YSTvlYfXmpvYSEWZLlotPKle6IDJX3qpZh6g-nB1-H-bCVLxTCVdp30JEx1__9O3nexl2uICx6kH505GkDR5iF9XVtP373yofj48_T2wkc2vsJM8IfLHW5Um4_jeo0LqTYxLbTQiAErzgOAkaNBsgQahzy_7NuQTJQuRqwjzw4Buig3VGOw7XyBOWQ7oWnjK1BhR8AKp393jiqC_7Yv8wPsmhAv7PpsNYJy8m2p6KGuYqEEgZ-xApf3WgKxUD3OYZbfjK-Vd3uKMp49r39G5Tww",
        "p": "xHHpPvNajCCuc2cwF34r7DEjN7BwHQRqhbwbAxtzQfSeZbh4aa7QTUpQQCmzwhTK8pCj4BUkYZIA1NNsVFmB3YhauPAxeAiG4NXSmZMJDPLrm0BEYNfPqpyNmNgwAYsqZ4UbBQK_OCoB0UuEqbknUZgKkVsliSzaVGIgLmz6rmU",
        "q": "yZkAdbAfaGpnGweW3BmEmOBum7aJW4Zkw8WyseNLQBjjHyjiC0509lguiugQW8DUeD0L0D-Yq7EScZ-fRvdBHxYZ43Fa1otjVpjco5mHb7qIkihpwjeiPfk8ULz-3095cOuJ9wBSmzgoEGwTGIF_dVuI9zZV9ulyXGGMKSYw4wc",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "mrLYkSLnjS8T21vW88_8-wcC2efbub_rxVQUZMtcXfK11EjtJSdgQyxB9E3g9V9YSTvlYfXmpvYSEWZLlotPKle6IDJX3qpZh6g-nB1-H-bCVLxTCVdp30JEx1__9O3nexl2uICx6kH505GkDR5iF9XVtP373yofj48_T2wkc2vsJM8IfLHW5Um4_jeo0LqTYxLbTQiAErzgOAkaNBsgQahzy_7NuQTJQuRqwjzw4Buig3VGOw7XyBOWQ7oWnjK1BhR8AKp393jiqC_7Yv8wPsmhAv7PpsNYJy8m2p6KGuYqEEgZ-xApf3WgKxUD3OYZbfjK-Vd3uKMp49r39G5Tww",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://academia.aulanet.com.bo/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "IZjZwOS3NQX8EKAzATkFGrmJ"
    }
]


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.aulanet.com.bo"]

# This url must not be None and should not be used anywhere
LEARNING_MICROFRONTEND_URL = "http://learn.openedx.org"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common LMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("LMS_BASE"),
    FEATURES["PREVIEW_LMS_BASE"],
    "lms",
]

MIDDLEWARE.insert(0, "whitenoise.middleware.WhiteNoiseMiddleware")


# Properly set the "secure" attribute on session/csrf cookies. This is required in
# Chrome to support samesite=none cookies.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
DCS_SESSION_COOKIE_SAMESITE = "None"


# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

