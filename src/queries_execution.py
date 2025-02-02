import queries_db_script as q
from create_db_script import create_all_tables, connect_to_database
from api_data_retrieve import populate_tables


# check if tables exists
def check_tables_existence():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT COUNT(DISTINCT `table_name`) FROM `information_schema`.`columns` WHERE `table_schema` = 'idorosiner'"
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    if result[0][0] == 0:
        return False
    return True


# run examples for query 1
def run_examples_for_query_1(cursor):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 1:")    
    cursor.execute(q.query_1('summer', '2017', 50000))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# run examples for query 2
def run_examples_for_query_2(cursor):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 2:")
    cursor.execute(q.query_2('Leonardo DiCaprio'))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# run examples for query 3
def run_examples_for_query_3(cursor):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 3:")
    cursor.execute(q.query_3('Inception'))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# run examples for query 4
def run_examples_for_query_4(cursor):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 4:")
    cursor.execute(q.query_4(8))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# run examples for query 5
def run_examples_for_query_5(cursor):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 5:")
    cursor.execute(q.query_5('adventure', 'Fantasy', '2020', '100'))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



if __name__ == '__main__':
    if not check_tables_existence():
        print("DB's tables does not exists - creating tables and inserting data to them now:")
        create_all_tables()
        populate_tables()
    
    connection = connect_to_database()
    cursor = connection.cursor()
    # run examples for all queries
    run_examples_for_query_1(cursor)
    run_examples_for_query_2(cursor)
    run_examples_for_query_3(cursor)
    run_examples_for_query_4(cursor)
    run_examples_for_query_5(cursor)
    connection.close()
