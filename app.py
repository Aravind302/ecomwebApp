from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import connect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import razorpay
import os

RAZORPAY_KEY_ID = 'rzp_test_HQ23jTnKGXPVtx'
RAZORPAY_KEY_SECRET = '2eW0kbTlIputPRzf5qrzIuG9'

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
verifyotp = "0"
db_config = {
    'host': 'localhost',
    'database': 'ecom12',
    'user': 'root',
    'password': 'root'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '06d9e48476f073fe40645f1ed1f3941fceb3abf97679a2778b7812252745805e'


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/home1")
def home1():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/verify")
def verify():
    return render_template("verifyemail.html")


@app.route("/verify1", methods=["POST", "GET"])
def verify1():
    otp = random.randint(1111, 9999)
    global verifyotp
    verifyotp = str(otp)
    print(verifyotp)

    if request.method == "POST":
        email = request.form['email']
        print("Sending Email")
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        mailusername = "aravindakki123@gmail.com"
        mailpassword = "xjcy bevq tdgw tahz"  # Remember to use an app-specific password
        from_email = mailusername
        to_email = email
        subject = 'OTP for Login'
        body = f"The OTP for verification is {otp}"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(mailusername, mailpassword)
            server.send_message(msg)
            server.quit()
            print("Email Sent")
            return render_template("enterotp.html", email=email)
        except Exception as e:
            print(f"Error in sending email: {e}")
            return render_template("result.html", message="Error in sending email.")
    else:
        return render_template("result.html", message="Data entered by unauthorized user.")


@app.route("/enterotp")
def enterotp():
    return render_template("enterotp.html")


@app.route("/verifyotp1", methods=["POST", "GET"])
def verifyotp1():
    if request.method == "POST":
        otp = request.form['otp']
        email = request.form['mail']
        if otp == verifyotp:
            return render_template("register.html", email=email)
        else:
            return render_template("result.html", message="Entered OTP was wrong. Please try again.")
    return render_template("result.html", message="Error occurred.")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register1", methods=["POST", "GET"])
def register1():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        mail = request.form['mail']
        username = request.form['username']
        password = request.form['password']
        try:
            conn = connect(**db_config)
            cursor = conn.cursor()
            q1 = "INSERT INTO user12 VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(q1, (fname, lname, mail, username, password))
            conn.commit()
        except Exception as e:
            return render_template("result.html", message=f"Error occurred: {str(e)}")
        finally:
            cursor.close()
            conn.close()

        return render_template("result.html", message="Registered Successfully. You can now log in.")
    return render_template("result.html", message="Error occurred.")


@app.route("/login1", methods=["POST", "GET"])
def login1():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            conn = connect(**db_config)
            cursor = conn.cursor()
            q1 = "SELECT * FROM user12 WHERE username = %s AND password = %s"
            cursor.execute(q1, (username, password))
            result = cursor.fetchone()

            if result:
                return render_template("userhome.html", mail=result[2])
            else:
                return render_template("result.html", message="Invalid Username or Password.")

        except Exception as e:
            return render_template("result.html", message=f"Error occurred: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    return render_template("result.html", message="Error occurred.")

@app.route("/storedata", methods=["POST", "GET"])
def storedata():
    if request.method == "POST":
        # Log the entire request form for debugging
        print(request.form)

        # Check if 'gather' is in form data
        if 'gather' not in request.form:
            return render_template("result.html", message="Missing cart data in the request.")

        details = request.form['gather']
        
        try:
            # Split the incoming cart data and validate length
            details_list = details.split(",")
            if len(details_list) != 5:
                return render_template("result.html", message="Invalid cart data format. Expected format: id,pname,price,email,quantity.")

            id, pname, price, email, quantity = details_list
            print(id)
            print(pname)
            print(price)
            print(email)
            print(quantity)

            # Validate the price and quantity
            if not price.replace('.', '', 1).isdigit():  # Allow for float values
                return render_template("result.html", message="Price must be a valid number.")
            if not quantity.isdigit():  # Ensure quantity is an integer
                return render_template("result.html", message="Quantity must be a valid integer.")

            price = float(price)  # Convert to float for further processing
            quantity = int(quantity)  # Convert to integer for further processing

            # Database interaction
            conn = connect(**db_config)
            cursor = conn.cursor()
            
            # Check if the product already exists in the cart
            q = "SELECT PRODUCT_QUANTITY FROM CART12 WHERE PRODUCT_ID = %s AND USEREMAIL = %s"
            cursor.execute(q, (id, email))
            row = cursor.fetchone()
            
            if row:  # Product exists, update quantity
                existing_quantity = int(row[0])  # Existing quantity is stored as a string, convert to int
                new_quantity = existing_quantity + quantity  # Add the new quantity

                q = "UPDATE CART12 SET PRODUCT_QUANTITY = %s WHERE PRODUCT_ID = %s AND USEREMAIL = %s"
                cursor.execute(q, (new_quantity, id, email))
            else:  # New product, insert it into the cart
                q = "INSERT INTO CART12 (PRODUCT_ID, PRODUCT_NAME, PRODUCT_PRICE, USEREMAIL, PRODUCT_QUANTITY) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(q, (id, pname, price, email, quantity))
            
            conn.commit()
            cursor.close()
            conn.close()

            return render_template("userhome.html", mail=email)

        except Exception as e:
            print(f"Error: {e}")
            return render_template("result.html", message="Error occurred in the database.")
        
    return render_template("result.html", message="Data not sent to backend, try again.")

@app.route("/storecart1", methods=["POST", "GET"])
def storecart1():
    if request.method == "POST":
        data = request.form['cart']  # Expecting a CSV format of cart data
        rows = data.split(",")

        if len(rows) < 5:
            return render_template("result.html", message="Insufficient data received.")

        # Extract product details from the cart data
        product_id = rows[0]
        product_name = rows[1]
        product_price = rows[2]
        user_email = rows[3]
        product_quantity = rows[4]

        try:
            # Convert the product price to float and quantity to int for calculations
            total_price = float(product_price) * int(product_quantity)
            total_price_paise = int(total_price * 100)  # Convert to paise for Razorpay

            # Create an order using Razorpay client
            order = client.order.create({
                'amount': total_price_paise,
                'currency': 'INR',
                'payment_capture': '1'  # Auto capture the payment
            })

            # Prepare the product data for rendering in the table
            product_info = [[product_id, product_name, product_price,user_email, product_quantity]]
            print(product_info)

            # Pass the product info and the order details to the template
            return render_template("showproducts.html", data=product_info, total=total_price, order=order)

        except Exception as e:
            print(f"Error in processing payment: {e}")
            return render_template("result.html", message="Error occurred in processing payment.")

    return render_template("result.html", message="Data not sent to backend, try again.")

@app.route("/showproducts", methods=["POST", "GET"])
def showproducts():
    if request.method == "POST":
        # Check if 'mail' is in the request form
        if 'mail' not in request.form:
            return render_template("result.html", message="Missing email in the request.")

        email = request.form['mail']

        # Log the received email to confirm it's correct
        print(f"Received email: {email}")

        try:
            conn = connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM CART12 WHERE USEREMAIL = %s"
            cursor.execute(q, (email,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            # Check if there are rows in the cart
            if not rows:
                return render_template("result.html", message="No items found in the cart.", status_code=404)

            # Log the fetched rows for debugging
            print(f"Fetched rows: {rows}")

            prices = []
            quantities = []
            for row in rows:
                prices.append(float(row[2]))  # PRODUCT_PRICE
                quantities.append(int(row[4]))  # PRODUCT_QUANTITY

            total_price = sum(price * quantity for price, quantity in zip(prices, quantities))
            total_price_paise = int(total_price * 100)  # Convert to paise for Razorpay
            
            # Log the total price to verify it's calculated correctly
            print(f"Total Price: {total_price}")

            # Create an order using Razorpay client
            order = client.order.create({
                'amount': total_price_paise,
                'currency': 'INR',
                'payment_capture': '1'  # Auto capture the payment
            })

            # Log the created order for debugging
            print(f"Razorpay Order: {order}")

            return render_template("showproducts.html", data=rows, total=total_price, order=order)
        
        except Exception as e:
            print(f"Error fetching cart items: {e}")
            return render_template("result.html", message=f"Error fetching cart items: {str(e)}")

    return render_template("result.html", message="Invalid request method. Please use POST.")



@app.route("/success", methods=["POST", "GET"])
def success():
    payment_id = request.form.get('razorpay_payment_id')
    order_id = request.form.get('razorpay_order_id')
    signature = request.form.get('razorpay_signature')

    dict1 = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        client.utility.verify_payment_signature(dict1)
        return render_template("result.html", message="Payment Successful")
    except razorpay.errors.SignatureVerificationError:
        return render_template("result.html", message="Payment Unsuccessful")


if __name__ == "__main__":
    app.run(port=5884)
