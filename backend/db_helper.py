import mysql.connector

cnx=mysql.connector.connect(
    host="localhost",
    user="root",
    password="", # your password for mysql
    database="pandeyji_eatery",
)

def insert_order_item(food_item,quantity,order_id):
    try:
        cursor=cnx.cursor()
        cursor.callproc('insert_order_item',(food_item,quantity,order_id))
        cnx.commit()
        cursor.close()
        return 1
    except mysql.connector.Error as err:
        cnx.rollback()
        return -1
    except Exception as e:
        cnx.rollback()
        return -1

def get_next_order_id():
    cursor=cnx.cursor()
    query="SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result=cursor.fetchone()[0]
    cursor.close()

    if result is None:
        return 1
    else:
        return result+1


def get_total_order_price(ordder_id):
    cursor=cnx.cursor()
    query=f"SELECT get_total_order_price({ordder_id})"
    cursor.execute(query)
    result=cursor.fetchone()[0]
    cursor.close()
    return  result

def get_order_status(order_id: int):
    # Create a cursor object
    cursor=cnx.cursor()

    # Write the SQL query
    query=("SELECT status from order_tracking WHERE order_id = %s")

    # Execute the query
    cursor.execute(query,(order_id,))

    # Fetch the result
    result=cursor.fetchone()

    # close the cursor and connection
    cursor.close()

    if result is not None:
        return result[0]
    else:
        return None

def insert_order_tracking(order_id,status):
    cursor = cnx.cursor()

    # Write the SQL query
    insert_query = "INSERT INTO order_tracking (order_id,status) VALUES (%s,%s)"

    # Execute the query
    cursor.execute(insert_query, (order_id,status))
    cnx.commit()

    # close the cursor and connection
    cursor.close()


