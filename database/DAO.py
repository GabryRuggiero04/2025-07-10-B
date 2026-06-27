from database.DB_connect import DBConnect
from model import category
from model.category import Category
from model.products import Product


class DAO():


    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT c.category_id, c.category_name 
                    FROM categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllProducts():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM products p  """

        cursor.execute(query)

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(categoryID):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.product_id 
                        FROM categories c 
                        join products p on c.category_id = p.category_id 
                        where c.category_id=  %s   """

        cursor.execute(query, (categoryID, ))

        for row in cursor:
            results.append(row["product_id"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(date1, date2, categoryId):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t1.idProdotto1, t2.idProdotto2, t1.peso1, t2.peso2
                    from(SELECT p.product_id as idProdotto1, sum(oi.quantity) as peso1
                            FROM products p
                            join order_items oi on p.product_id = oi.product_id
                            JOIN orders o on o.order_id = oi.order_id
                            and o.order_date BETWEEN %s and %s
                            and p.category_id=%s
                            group BY p.product_id) t1
                    join (SELECT p2.product_id as idProdotto2, sum(oi2.quantity) as peso2
                            FROM products p2
                            join order_items oi2 on p2.product_id = oi2.product_id
                            JOIN orders o2 on o2.order_id = oi2.order_id
                            and o2.order_date BETWEEN %s and %s
                            and p2.category_id=%s
                            GROUP BY p2.product_id) t2 on t1.idProdotto1<t2.idProdotto2  """

        cursor.execute(query, (date1, date2, categoryId, date1, date2, categoryId, ))

        for row in cursor:
            results.append((row["idProdotto1"],
                            row["idProdotto2"],
                            row["peso1"],
                            row["peso2"]))

        cursor.close()
        conn.close()
        return results