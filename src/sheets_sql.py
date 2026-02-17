import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from mysql import connector
import pandas as pd
import os
import numpy as np
import mysql

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]