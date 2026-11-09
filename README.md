# ShopZen -- E-Commerce Website

## About the Project

ShopZen is an e-commerce website where customers can create an account,
log in, browse products, add items to their cart, and place orders.

Customers can use **Add to Cart** to buy multiple products or **Buy
Now** to purchase one product directly. The current checkout supports
Cash on Delivery (COD).

## Technologies Used

  -----------------------------------------------------------------------
  Technology                          Why I Used It
  ----------------------------------- -----------------------------------
  Python                              To write the backend logic of the
                                      application.

  Django                              To handle login, product pages,
                                      cart operations, and orders.

  HTML                                To create the structure of website
                                      pages.

  CSS                                 To style the pages and improve
                                      their appearance.

  Bootstrap                           To make the website responsive and
                                      create buttons, forms, and
                                      navigation bars easily.

  MySQL                               To store product and order
                                      information.
  -----------------------------------------------------------------------

## Main Features

-   User registration and login
-   Browse and search products
-   Filter products by category and price
-   Add products to cart
-   Buy Now option
-   Checkout and delivery details
-   Cash on Delivery
-   Order success page
-   Admin product management and dashboard

## How to Use the Website

1.  Open the ShopZen website.
2.  Click **Sign Up** if you are a new user.
3.  Enter your details and create an account.
4.  Go to the Login page and enter your username and password.
5.  Browse products on the home page.
6.  Click **Add to Cart** or **Buy Now**.
7.  Enter your delivery details at checkout.
8.  Place your order and view the order success page.

**Note:** Users must log in before using the cart and checkout features.
The current project supports Cash on Delivery; an online payment gateway
is not included.

## Simple Flowcharts

GitHub displays these Mermaid diagrams as visual flowcharts when this
file is saved as `README.md`.

### 1. Signup and Login

``` mermaid
flowchart TD
    A([Start]) --> B[Open ShopZen]
    B --> C{Have an account?}
    C -->|No| D[Sign Up]
    D --> E[Enter Details]
    E --> F[Create Account]
    F --> G[Login]
    C -->|Yes| G
    G --> H[Enter Username and Password]
    H --> I{Correct Details?}
    I -->|No| G
    I -->|Yes| J[Home Page]
    J --> K([End])
```

### 2. Shopping and Checkout

``` mermaid
flowchart TD
    A([Start]) --> B[Login]
    B --> C[Browse Products]
    C --> D[Select Product]
    D --> E{Choose Option}
    E -->|Add to Cart| F[Open Cart]
    F --> G[Proceed to Checkout]
    E -->|Buy Now| H[Go to Checkout]
    G --> I[Enter Delivery Details]
    H --> I
    I --> J[Place Order]
    J --> K[Order Success]
    K --> L([End])
```

### 3. Project Setup

``` mermaid
flowchart TD
    A([Start]) --> B[Download or Clone Project]
    B --> C[Open Project Folder]
    C --> D[Create Virtual Environment]
    D --> E[Activate Environment]
    E --> F[Install Requirements]
    F --> G[Create MySQL Database]
    G --> H[Configure .env]
    H --> I[Run Migrations]
    I --> J[Create Admin Account]
    J --> K[Run Django Server]
    K --> L[Open Website]
    L --> M([End])
```

## Project Setup

### Step 1: Clone the Project

``` bash
git clone https://github.com/nveerababu/ShopZen.git
cd ShopZen
```

Open the folder that contains `manage.py`.

### Step 2: Create a Virtual Environment

**macOS:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

``` powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install Packages

``` bash
pip install -r requirements.txt
```

### Step 4: Create a MySQL Database

Open MySQL and create the database:

``` sql
CREATE DATABASE Shopzen_db;
```

### Step 5: Configure the `.env` File

Create `.env` in the same folder as `manage.py`. Add your own settings:

``` env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=Shopzen_db
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

Use the database and email values that match your own setup. Do not
upload `.env` or real passwords to GitHub.

### Step 6: Run Database Migrations

``` bash
python manage.py migrate
```

### Step 7: Create an Admin Account

``` bash
python manage.py createsuperuser
```

Follow the prompts to create your admin username and password.

### Step 8: Start the Website

``` bash
python manage.py runserver
```

Open this address in your browser:

`http://127.0.0.1:8000/`

## Project Folder Structure

``` text
ShopZen/
├── ShopZen/
│   ├── settings.py
│   └── urls.py
├── testapp/
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## My Learning

While building ShopZen, I learned how to create web pages, connect the
frontend with Django, work with a MySQL database, manage user login,
handle cart operations, and process customer orders.

------------------------------------------------------------------------

**Project:** ShopZen\
**Type:** E-Commerce Website\
**Backend:** Python and Django\
**Frontend:** HTML, CSS and Bootstrap\
**Database:** MySQL\
**Payment:** Cash on Delivery (COD)
