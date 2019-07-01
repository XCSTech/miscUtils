import sql3
import configparser


def msParams():
    config = configparser.ConfigParser()
    config.read('test.ini')
    host    = config['mssql']['host']
    user    = config['mssql']['user']
    passwd  = config['mssql']['passwd']
    db      = config['mssql']['db'] if len(config['mssql']['db']) > 0 else None
    extra   = [ {'autocommit':True} ]
    return [host, user, passwd, db]

def connectMs():
    run = sql3.mssql(*[ param for param in  msParams() ])
    return run

def closeMs(run):
    run.close()

def test_mysql_connection():
    run = connectMs()
    closeMs(run)

#def test_execute_query():
#    run = connectMs()
#    
#    if 'test_db' in [database['name'] for database in run.query('SELECT name FROM master.dbo.sysdatabases')]:
#        run.query("""DROP DATABASE test_db""")
#
#    ## Create Database
#    run.query(f"""
#        CREATE      DATABASE test_db;
#    """)
#    assert 'test_db' in [database['name'] for database in run.query('SELECT name FROM master.dbo.sysdatabases')]
#
#    ## Create table
#    run.query(f"""
#        USE         test_db;
#    """)
#    run.query(f"""
#        CREATE      TABLE test_table
#        (
#                    example varchar(45)
#        );
#    """)
#    assert 'test_table' in [table['table_name'] for table in run.query('SELECT table_name FROM information_schema.tables')]
#
#    ## Insert data into table
#    run.query(f"""
#        INSERT      INTO test_table 
#                    (example) 
#                    VALUES 
#                    (%s);
#    """,'test')
#    num = run.query(f"""
#        SELECT      COUNT(*) as c
#        FROM        test_table
#        WHERE       example = %s
#    """,'test')[0]['c']
#    assert num == 1
#
#    ## Drop db if all successful
#    run.query(f"""
#        DROP        DATABASE IF EXISTS test_db
#    """)
#    closeMs(run)
