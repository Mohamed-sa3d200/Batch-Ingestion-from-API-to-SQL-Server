import pyodbc
from config import *

def get_connection():

    return pyodbc.connect(
        f"""
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={SERVER};
        DATABASE={DATABASE};
        Trusted_Connection=yes;
        """
    )