#!/usr/bin/env python

from cassandra.cluster import Cluster
import sys
import csv
import os

if len(sys.argv) < 2:
    print "ERROR: Keyspace name not provided."
    exit(1)
else:
    keyspace_name = sys.argv[1]

schema_query = '''SELECT * FROM system_schema.tables \
                WHERE keyspace_name=%s;'''

columns_query = '''SELECT keyspace_name, table_name, column_name \
                FROM system_schema.columns WHERE keyspace_name=%s'''

du_command = "echo 'size_on_disk',`du -hc /var/lib/cassandra/data/%s/%s* \
            | grep total | awk '{print $1}'`"

def setup():
    cluster = Cluster()
    session = cluster.connect()
    return session

def generate_csv(dlist):
    for d in dlist:
        name = d['table_name'] + ".csv"
        with open(name, 'wb') as f:
            w = csv.writer(f)
            w.writerows(d.items())
        f.close()

def add_table_size(dicts):
    # Using os instead of subprocess because I miss 2.6...
    for thing in dicts:
        out = os.popen(du_command % (thing['keyspace_name'], thing['table_name']))
        a = out.read().rstrip()
        vals = a.split(",")
        thing[vals[0]] = vals[1]
    return dicts

def get_table_schemas(session, keyspace_name):
    result = session.execute(schema_query, (keyspace_name,))
    dicts = []
    for a in result:
        a = a.__dict__
        dicts.append(a)
    return dicts

def add_columns():
    pass

def profile_tables(session, keyspace_name):
    a = get_table_schemas(session, keyspace_name)
    # b = add_columns(a)
    c = add_table_size(a)
    return c

if __name__ == "__main__":
    session = setup()
    dicts = profile_tables(session, keyspace_name)
    generate_csv(dicts)
