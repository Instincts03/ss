import argparse
import datetime
import http.client
import io
import json
import logging
import logging.config
import os
import re
import shutil
import statistics
import time
import warnings
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from itertools import permutations
import numpy as np
import pandas as pd
import psycopg2
import pytz
import requests
import urllib3
#from bs4 import BeautifulSoup
#from fuzzywuzzy import process
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from sqlalchemy import create_engine
from tqdm import tqdm

warnings.filterwarnings("ignore")
