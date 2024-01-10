import mysql.connector
from settings_local import settings
import logging
from util import infomessage, validate_db_arg_input
import json
import sys
from setup_config import setup_config

mod_logger = logging.getLogger(__name__)

# Connection to database
def get_connection():
    db_to_use=validate_db_arg_input(sys.argv)
    infomessage(mod_logger,f"Connecting to:{settings['database'][db_to_use]['database']}")
    try:
        conn = mysql.connector.connect(**settings["database"][db_to_use])
        return conn
    
    except mysql.connector.Error as e:
        infomessage(mod_logger,"An error ocurred, see log")
        mod_logger.error(e)
        sys.exit()

    except Exception as ex:
        infomessage(mod_logger,"An exception ocurred, see log")
        mod_logger.exception(ex)
        sys.exit()

def exec_sql(sql :str,db_conn :mysql.connector.connection,many :list=None, one :tuple=None):
    try:
        db_cur=db_conn.cursor()
        if many:
            db_cur.executemany(sql,many) 
        else:
            db_cur.execute(sql,one)

        db_conn.commit()
    
    except Exception as ex:
        infomessage(mod_logger,"An exception ocurred, see log")
        mod_logger.exception(ex)
    
    finally:
        if db_cur:
            db_cur.close()

def delete_table(table_name, db_conn :mysql.connector.connection):
    try:
        query = "DROP TABLE {}".format(table_name)

        exec_sql(query, db_conn)
        
        infomessage(mod_logger,"Table {} deleted successfully".format(table_name))

    except Exception as ex:
        mod_logger.exception(ex)

def save_homework(homework :list,db_conn :mysql.connector.connection):
    sql = """INSERT INTO homework (childid,firstname,homework) 
    VALUES (%s,%s,%s)"""

    for i,hw in enumerate(homework, start=1):
        #f"Saving homework for {i} of {len(homework)} child{"ren" if len(homework)>1 else ""}"
        infomessage(mod_logger,"Saving homework {}".format(i))

        try:
            db_tuple=(settings["children"][hw["name"]]["id"], hw["name"],json.dumps(hw))

        except Exception as ex:
            mod_logger.exception(ex)

        try:
            exec_sql(sql,db_conn,one=db_tuple)

        except Exception as ex:
            mod_logger.exception(ex)
            infomessage(mod_logger,"EX: Homework NOT SAVED")


def save_weekplan(weekplans : list, db_conn :mysql.connector.connection):
    sql = """INSERT INTO weekplan (childid,firstname,weekplan) 
    VALUES (%s,%s,%s)"""

    number_of_plans=len(weekplans)

    for i,wp in enumerate(weekplans, start=1):
        #f"Saving homework for {i} of {len(homework)} child{"ren" if len(homework)>1 else ""}"
        infomessage(mod_logger,"Saving weekplan {} of {}: {}".format(i,number_of_plans,wp["name"]))

        try:
            db_tuple=(settings["children"][wp["name"]]["id"], wp["name"],json.dumps(wp))

        except Exception as ex:
            mod_logger.exception(ex)

        try:
            exec_sql(sql,db_conn,one=db_tuple)

        except Exception as ex:
            mod_logger.exception(ex)
            infomessage(mod_logger,"EX: weekplan NOT SAVED")


def setup():
    """WARNING : THIS FUNCTION DELETES ALL TABLES if they exist and creates them empty again
    
    Tables are defined in the setup_config.py file"""
    
    tables=', '.join(table for table in setup_config["tables"].keys())
    sql = f"DROP TABLE IF EXISTS {tables}"
    db_conn, db_cur = get_connection()

    # DROPPING TABLES
    infomessage(mod_logger,f"SETUP HAS STARTED")
    infomessage(mod_logger,f"Dropping tables: {tables}")
    try:
       
        db_cur.execute(sql)
        db_conn.commit()

    except Exception as ex:
        mod_logger.exception(ex)
        infomessage(mod_logger,"Failed to drop tables")
        if db_conn.is_connected():
            db_cur.close()
            db_conn.close()
        sys.exit(1)
    else:
        infomessage(mod_logger,f"Tables {tables} DROPPED")

    # CREATING TABLES
    infomessage(mod_logger,f"Creating tables")
    try:
        for table,sql in setup_config["tables"].items():
            infomessage(mod_logger,f"Creating '{table}'")
            db_cur.execute(sql)

        db_conn.commit()

    except mysql.connector.Error as err:
        mod_logger.error(err)
        infomessage(mod_logger,f"Create tables failed, error: {err}")
        sys.exit(1)

    except Exception as ex:
        mod_logger.exception(ex)
        print(f"Create tables failed, exception: {ex}")
        sys.exit(1)

    else:
        infomessage(mod_logger,f"Tables created'{table}'")

    if db_conn:
        db_conn.close()
        db_cur.close()
    infomessage(mod_logger,f"SETUP COMPLETE")

