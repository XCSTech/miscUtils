import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
import sql3
import configparser

def liteParam():
    config = configparser.ConfigParser()
    config.read('test.ini')
    path    = config['sqlite']['path']
    return path

def query_commands(run):
    ## Create table
    run.query(f"""
        CREATE      TABLE test_table
        (
                    example text
        );
    """)
    assert 'test_table' in [table['name'] for table in run.query('SELECT name FROM sqlite_master WHERE type = "table"')]

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
        DROP        TABLE test_table;
    """)
    run.commit()

def connectLite():
    run = sql3.sqlite(liteParam())
    return run

def closeLite(run):
    run.close()

def test_lite_connection():
    run = connectLite()
    closeLite(run)

def test_decorator():

    @sql3.liteCon(liteParam())
    def running(run):
        query_commands(run)
        return True

    assert running()

def test_execute_query():
    run = connectLite()
    query_commands(run)
    closeLite(run)
