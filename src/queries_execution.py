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
def run_examples_for_query_1():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 1:")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    q.query_1('summer', '2023', 500000)


# run examples for query 2
def run_examples_for_query_2():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 2:")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    q.query_2('Leonardo DiCaprio')


# run examples for query 3
def run_examples_for_query_3():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 3:")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    q.query_3('Inception')


# run examples for query 4
def run_examples_for_query_4():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 4:")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    q.query_4(8)


# run examples for query 5
def run_examples_for_query_5():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("query 5:")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    q.query_5('adventure', 'Action', '2020', '120')



if __name__ == '__main__':
    if not check_tables_existence():
        print("DB's tables does not exists - creating tables and inserting data to them now:")
        create_all_tables()
        populate_tables()

    # run examples for all queries
    run_examples_for_query_1()
    run_examples_for_query_2()
    run_examples_for_query_3()
    run_examples_for_query_4()
    run_examples_for_query_5()
