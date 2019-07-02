class mysql(object):

    def __init__(self, host, user, passwd, db=None, **kwargs):
        ## Initiate connection
        import pymysql
        self.con = pymysql.connect(
                host=host,
                user=user,
                password=passwd,
                db=db,
        )
        self.x = self.con.cursor(pymysql.cursors.DictCursor)

    def close(self):
        ## Close connections
        self.x.close()
        self.con.close()

    def query(self, query, *args):
        ## Run query and return result
        try:
            self.x.execute( query, (args) )
            return self.x.fetchall()
        except Exception as e:
            raise Exception(f"""
                Error: {str(e)}\n
                \n
                {self._executed()}
            """)

    def _executed(self):
        ## Return executed query
        return self.x._executed

    def commit(self):
        ## Commit changes
        self.con.commit()

def mysqlCon(*parameters):
    def wrap(f):
        def wrapper(*args, **kwargs):
            run = mysql(*parameters)
            value = f(run, *args, **kwargs)
            run.close()
            return value
        return wrapper
    return wrap


class mssql(object):
    
    def __init__(self, host, user, passwd, db=None):
        ## Initiate connection
        import pymssql
        self.con = pymssql.connect(host=host, user=user, password=passwd, database=db, charset="ISO-8859-1")
        self.x = self.con.cursor(as_dict=True)

    def close(self):
        ## Close connection
        self.x.close()
        self.con.close()

    def query(self, query, *args):
        ## Run query and return result
        try:
            self.x.execute( query, (args) )
            return self.x.fetchall()
        except Exception as e:
            raise Exception(f"""
                Error: {str(e)}\n
                \n
                {query}
            """)

    def commit(self):
        ## Commit changes
        self.con.commit()


def mssqlCon(*parameters):
    def wrap(f):
        def wrapper(*args, **kwargs):
            run = mssql(*parameters)
            value = f(run, *args, **kwargs)
            run.close()
            return value
        return wrapper
    return wrap

class sqlite(object):
    
    def __init__(self, path):
        # Initiate sqlite3 connection
        print(path)
        import sqlite3
        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row
        self.x = self.con.cursor()

    def close(self):
        # Close sqlite3 connection
        self.x.close()
        self.con.close()

    def query(self, query, *args):
        # Make query
        self.x.execute( query.replace('%s','?'), (args) )
        return self.x.fetchall()

    def commit(self):
        ## Commit changes
        self.con.commit()

def liteCon(path):
    def wrap(f):
        def wrapper(*args, **kwargs):
            run = sqlite(path)
            value = f(run, *args, **kwargs)
            run.close()
            return value
        return wrapper
    return wrap
