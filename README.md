Ecommerce-Web-Application

Developed intuitive web pages, implemented secure email verification with Python SMTP, and designed user authentication. Built a dynamic cart system with total price calculation and integrated Razorpay for secure payment processing.
To explain how the e-commerce application functions step by step:

User Registration and Login:

Users access the home page, where they can navigate to the registration page. On the registration page, users fill out their details. Before the registration is complete, the system sends an OTP (One-Time Password) to the user's email using Python's SMTP module. The user enters the OTP to verify their email and complete the registration process. After successful registration, the user can log in using the login page.

User Home and Product Display:

After logging in, the user is directed to the user home page. The "show products" page allows users to browse through available products.

Shopping Cart Functionality:

Users can select products they wish to purchase, and the items are added to a dynamic shopping cart. The cart page displays the selected products, calculates the total price for each item (based on quantity), and shows a grand total for all items in the cart.

Payment Integration:

When ready to purchase, users proceed to the payment page, where the Razorpay payment gateway is integrated. The user completes the payment via Razorpay, and the transaction details are securely stored in the MySQL database.

Order Confirmation:

After successful payment, the system confirms the order and notifies the user via email or on the website that the transaction is complete.

This flow provides a smooth e-commerce experience, from user registration to payment processing.

