import sys
sys.path.append('..')
import sql3
import configparser

def myParams():
    config = configparser.ConfigParser()
    config.read('test.ini')
    host    = config['mysql']['host']
    user    = config['mysql']['user']
    passwd  = config['mysql']['passwd']
    db      = config['mysql']['db'] if len(config['mysql']['db']) > 0 else None
    return [host, user, passwd, db]

def query_commands(run):
    if 'test_db' in [database['Database'] for database in run.query('SHOW DATABASES')]:
        run.query("""DROP DATABASE test_db""")

    ## Create Database
    run.query(f"""
        CREATE      DATABASE test_db;
    """)
    assert 'test_db' in [database['Database'] for database in run.query('SHOW DATABASES')]

    ## Create table
    run.query(f"""
        USE         test_db;
    """)
    run.query(f"""
        CREATE      TABLE test_table
        (
                    example varchar(45)
        );
    """)
    assert 'test_table' in [table['Tables_in_test_db'] for table in run.query('SHOW TABLES')]

    ## Insert data into table
    run.query(f"""
        INSERT      INTO test_table 
                    (example) 
                    VALUES 
                    (%s);
    """,'test')
    num = run.query(f"""
        SELECT      COUNT(*) as c
        FROM        test_table
        WHERE       example = %s
    """,'test')[0]['c']
    assert num == 1

    ## Drop db if all successful
    run.query(f"""
        DROP        DATABASE IF EXISTS test_db
    """)

def connectMy():
    run = sql3.mysql(*[ param for param in  myParams() ])
    return run

def closeMy(run):
    run.close()

def test_mysql_connection():
    run = connectMy()
    closeMy(run)

def test_decorator():

    @sql3.mysqlCon(*[ param for param in  myParams() ])
    def running(run):
        query_commands(run)
        return True

    assert running()

def test_execute_query():
    run = connectMy()
    query_commands(run)
    closeMy(run)
