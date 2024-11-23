from faker import Faker
import mysql.connector
from mysql.connector import Error
import random

faker = Faker()

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='e_commerce_SQL',
        user='root',
        password=''
    )
    if connection.is_connected():
        cursor = connection.cursor()

        for _ in range(10):
            username = faker.user_name()
            password = faker.password()
            email = faker.email()
            cursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", 
                           (username, password, email))
            user_id = cursor.lastrowid

            street = faker.street_address()
            city = faker.city()
            country = faker.country()
            postal_code = faker.postcode()
            cursor.execute("INSERT INTO address (user_id, street, city, country, postal_code) VALUES (%s, %s, %s, %s, %s)",
                           (user_id, street, city, country, postal_code))

        for _ in range(20):
            name = faker.word()
            description = faker.sentence()
            price = round(random.uniform(5.00, 100.00), 2)
            stock = faker.random_int(min=1, max=50)
            cursor.execute("INSERT INTO product (name, description, price, stock) VALUES (%s, %s, %s, %s)",
                           (name, description, price, stock))
            product_id = cursor.lastrowid

        for _ in range(5):
            user_id = random.randint(1, 10)
            for _ in range(random.randint(1, 3)):
                product_id = random.randint(1, 20)
                quantity = random.randint(1, 5)
                cursor.execute("INSERT INTO cartproductlist (product_id, quantity) VALUES (%s, %s)", 
                               (product_id, quantity))
                cartproductlist_id = cursor.lastrowid

                cursor.execute("INSERT INTO cart (user_id, cartproductlist_id) VALUES (%s, %s)",
                               (user_id, cartproductlist_id))
                cart_id = cursor.lastrowid

                status = random.choice(['Pending', 'Completed', 'Cancelled'])
                cursor.execute("INSERT INTO command (cart_id, status) VALUES (%s, %s)", 
                               (cart_id, status))
                command_id = cursor.lastrowid

                total_amount = round(random.uniform(50.00, 500.00), 2)
                payment_status = random.choice(['Paid', 'Unpaid'])
                cursor.execute("INSERT INTO invoice (command_id, total_amount, payment_status) VALUES (%s, %s, %s)",
                               (command_id, total_amount, payment_status))

            payment_method = random.choice(['Credit Card', 'PayPal', 'Bank Transfer'])
            details = faker.credit_card_number() if payment_method == 'Credit Card' else faker.text(20)
            cursor.execute("INSERT INTO payment (user_id, payment_method, details) VALUES (%s, %s, %s)",
                           (user_id, payment_method, details))

        for _ in range(10):
            user_id = random.randint(1, 10)
            product_id = random.randint(1, 20)
            photo_url = faker.image_url()
            cursor.execute("INSERT INTO photo (user_id, product_id, photo_url) VALUES (%s, %s, %s)",
                           (user_id, product_id, photo_url))

            rating = random.randint(1, 5)
            review = faker.sentence()
            cursor.execute("INSERT INTO rate (user_id, product_id, rating, review) VALUES (%s, %s, %s, %s)",
                           (user_id, product_id, rating, review))

        connection.commit()

except Error as e:
    print("Erreur lors de la connexion à MySQL", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
