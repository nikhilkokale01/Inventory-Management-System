# app.py
import base64
import datetime
import time

# from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin

from flask import render_template, redirect, url_for, request, flash, Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'Define_The_Key'


# login_manager = LoginManager(app)

# app.py (continuation)
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50))
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50), nullable=False)
    loc_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    location = relationship("Location", back_populates="userlocation")
    orders = relationship('Order', back_populates='customer')
    # Relationship with orders, and set cascade='all, delete-orphan'
    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')

    def get_orders(self):
        return Order.query.filter_by(user_id=self.id).all()

# class Customer(db.Model):
#     __tablename__ = "customer"
#     id = db.Column(db.Integer, primary_key=True)
#     firstName = db.Column(db.String(50), nullable=False)
#     middleName = db.Column(db.String(50), nullable=False)
#     lastName = db.Column(db.String(50), nullable=False)
#     userName = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(50), nullable=False)


class Employees(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    job = relationship("Job", back_populates="jobEmployee")

    loc_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    location = relationship("Location", back_populates="emplocation")

    def get_users_from_same_location(self):
        return Users.query.filter_by(location_id=self.location_id).all()

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.today().date())
    customer = relationship('Users', back_populates='orders')
    product = relationship('Product', back_populates='orders')
    delivered = db.Column(db.Boolean, default=False)

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    jobEmployee = relationship("Employees", back_populates="job")


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    emplocation = relationship("Employees", back_populates="location")
    userlocation = relationship("Users", back_populates="location")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100))
    productImg = db.Column(db.LargeBinary)
    productDiscription = db.Column(db.String(255))
    productPrice = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    # productCategory = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship("Category", back_populates="product")

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = relationship("Supplier", back_populates="product")
    orders = relationship('Order', back_populates='product')


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    product = relationship("Product", back_populates="category")





class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.Integer)
    product = relationship("Product", back_populates="supplier")


#db.create_all()


@app.route('/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('loginUsername')
        password = request.form.get('loginPassword')
        user = Users.query.filter_by(userName=username).first()
        password = Users.query.filter_by(password=password).first()
        if not user:
            flash('username does not exist', 'error')
            # if user and user.check_password(password):
        #     login_user(user)
        elif not password:
            flash("password doesn't match")
            # flash('Logged in successfully.', 'success')
            # return redirect(url_for('index'))
        else:
            flash('Logged in successfully.', 'success')
            # time.sleep(2)
            session['user_id'] = user.id
            return redirect(url_for('home'))
            # flash('Invalid username or password.', 'error')
    locations = Location.query.all()
    return render_template('login.html', locations=locations)


@app.route('/home-page')
def home():
    categories = Category.query.all()
    products = Product.query.all()
    product = Product.query.filter_by(id=1).first()
    print(product.category.name)
    return render_template('user.html', products=products, categories=categories)


from flask import request, jsonify


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity', 1))

        product = Product.query.get(product_id)
        if product:
            if product.quantity >= quantity:
                # Update the quantity in the database
                product.quantity -= quantity
                db.session.commit()

                # Add the item to the cart
                cart_item = {
                    'id': product.id,
                    'name': product.productName,
                    'price': product.productPrice,
                    'quantity': quantity
                }
                session_cart = session.get('cart', [])
                session_cart.append(cart_item)
                session['cart'] = session_cart

                return jsonify({'success': True, 'message': 'Item added to cart successfully'})

            return jsonify({'success': False, 'message': 'Not enough quantity available'})

        return jsonify({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


from sqlalchemy.exc import IntegrityError


@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json

    user_id = data.get('userId')
    products = data.get('products', [])

    try:
        for product_data in products:
            product_id = product_data['productId']
            quantity = product_data['quantity']

            # Check if an order for the same product and user already exists
            existing_order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()

            if existing_order:
                # If an order exists, update the quantity
                existing_order.quantity += quantity
            else:
                # If no order exists, create a new order
                order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
                db.session.add(order)

        db.session.commit()
        return jsonify({'message': 'Order placed successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'IntegrityError - Duplicate key'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/get_orders', methods=['GET'])
def get_orders():
    # Assuming you have a User model with a relationship to the Order model
    user_id = 1  # Implement a function to get the current user ID
    user_orders = Order.query.filter_by(user_id=user_id).all()

    orders = [{'product': {'name': order.product.productName, 'price': order.product.productPrice}, 'quantity': order.quantity, 'delivered': order.delivered} for order in user_orders]
    return jsonify(orders)

@app.route('/get_products/<category_id>')
def get_products(category_id):
    # products = Product.query.all()
    products = Product.query.filter_by(category_id=category_id).all()

    products_list = [{'id': product.id, 'name': product.productName,
                      'description': product.productDiscription,
                      'price': product.productPrice, 'category': product.category.name,
                      'supplier': product.supplier.company_name,
                      'quantity': product.quantity,
                      'image': base64.b64encode(product.productImg).decode('utf-8') if product.productImg else None} for
                     product in products]
    # print(products_list)
    return jsonify(products_list)
    # return jsonify([{'id': product.id, 'name': product.productName, 'price': product.productPrice} for product in products])


@app.route('/user-register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        fname = request.form.get('firstName')
        mname = request.form.get('middleName')
        lname = request.form.get('lastName')
        uname = request.form.get('registerUsername')
        email = request.form.get('registerEmail')
        password = request.form.get('registerPassword')

        if Users.query.filter_by(userName=uname).first():
            flash("This username already exist!")
            return redirect(url_for('user_login'))
        elif Users.query.filter_by(email=email).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('user_login'))
        upload = Users(
            firstName=fname,
            middleName=mname,
            lastName=lname,
            userName=uname,
            email=email,
            password=password
        )
        db.session.add(upload)
        db.session.commit()
        flash('Logged in successfully.', 'success')
    return render_template('login.html')


@app.route('/employee', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        username = request.form.get('loginUsername')
        password = request.form.get('loginPassword')
        employee = Employees.query.filter_by(userName=username).first()
        password = Employees.query.filter_by(password=password).first()
        if not employee:
            flash('username does not exist', 'error')
            # if user and user.check_password(password):
        #     login_user(user)
        elif not password:
            flash("password doesn't match")
            # flash('Logged in successfully.', 'success')
            # return redirect(url_for('index'))
        else:
            flash('Logged in successfully.', 'success')
            time.sleep(2)
            curr = Employees.query.filter_by(userName=username).first()
            users_same_location = Users.query.filter_by(loc_id=curr.loc_id).all()
            return render_template('employee_interface.html', curr=curr, users_same_location=users_same_location, city=curr.location.city)
    return render_template('employee-login.html')


@app.route('/employee-register', methods=['GET', 'POST'])
def employee_register():
    if request.method == 'POST':
        fname = request.form.get('firstName')
        mname = request.form.get('middleName')
        lname = request.form.get('lastName')
        uname = request.form.get('registerUsername')
        email = request.form.get('registerEmail')
        password = request.form.get('registerPassword')
        if Employees.query.filter_by(userName=uname).first():
            flash("This username already exist!")
            return redirect(url_for('employee_login'))
        elif Employees.query.filter_by(email=email).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('employee_login'))
        upload = Employees(
            firstName=fname,
            middleName=mname,
            lastName=lname,
            userName=uname,
            email=email,
            password=password
        )
        db.session.add(upload)
        db.session.commit()
        curr = Employees.query.filter_by(userName=uname).first()

        users_same_location = Users.query.filter_by(loc_id=curr.loc_id).all()
        print(curr)
        # flash('Logged in successfully.', 'success')
        return render_template('employee_interface.html', curr=curr, users_same_location=users_same_location)
        # return render_template('employee_interface.html', curr=curr)
    return render_template('employee-login.html')


@app.route('/employee_interface')
def employee_interface(curr, users_same_location):
    return render_template('employee_interface.html', curr=curr, users_same_location=users_same_location)


# @app.route('/tasks')
# def tasks():
#     return render_template('tasks.html')


@app.route('/edit_employee/<int:employee_id>')
def edit_employee(employee_id):
    employee = Employees.query.get(employee_id)

    if employee:
        jobs = Job.query.all()
        locations = Location.query.all()
        return render_template('edit_employee.html', employee=employee, jobs=jobs, locations=locations)
    else:
        flash('Employee not found.', 'error')
        return redirect(url_for('dashboard'))
@app.route('/edit_product/<int:product_id>')
def edit_product(product_id):
    product = Product.query.get(product_id)
    print(product)
    if product:
        suppliers = Supplier.query.all()
        categories = Category.query.all()
        return render_template('edit_product.html', product=product, suppliers=suppliers, categories=categories)
    else:
        flash('Product not found.', 'error')
        return redirect(url_for('dashboard'))

from flask import jsonify

from flask import jsonify

@app.route('/update_employee/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    employee = Employees.query.get(employee_id)

    if employee:
        # Update the employee fields based on the form data
        employee.firstName = request.form.get('fName')
        employee.middleName = request.form.get('mName')
        employee.lastName = request.form.get('lName')
        employee.userName = request.form.get('uName')
        employee.email = request.form.get('email')
        employee.password = request.form.get('password')
        # Update other fields as needed

        try:
            db.session.commit()
            flash('Employee updated successfully!', 'success')
            return jsonify({'status': 'success'})
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        flash('Employee not found.', 'error')
        return jsonify({'status': 'error', 'message': 'Employee not found'})


@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product = Product.query.get(product_id)
    print(product)
    if product:
        # Update the employee fields based on the form data

        supplier_id = int(request.form.get('supplier'))
        category_id = int(request.form.get('category'))
        supplier = Supplier.query.filter_by(id=supplier_id).first()
        category = Category.query.filter_by(id=category_id).first()

        # file = request.files['file']
        # upload = Product(
        #     category=category,
        #     supplier=supplier
        # )
        print(request.form.get('productName'))
        product.productName = request.form.get('productName')
        product.productPrice = request.form.get('price')
        product.productDiscription = request.form.get('discription')
        product.productImg = product.productImg
        product.quantity = request.form.get('quantity')
        product.supplier = supplier
        product.category = category
        # db.session.commit()

        try:
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return jsonify({'status': 'success'})
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        flash('Employee not found.', 'error')
        return jsonify({'status': 'error', 'message': 'Employee not found'})


@app.route('/dashboard')
def index():
    data = {
        'username': 'John Doe',
        'analytics_data': [
            {'metric': 'Visitors', 'value': 1000},
            {'metric': 'Page Views', 'value': 5000},
            # Add more data as needed
        ]
    }
    return render_template('dashboard.html', data=data)


@app.route('/analytics')
def analytics():
    analytics_data = [
        {'metric': 'Clicks', 'value': 300},
        {'metric': 'Conversions', 'value': 25},
        # Add more analytics data as needed
    ]
    return render_template('analytics.html', analytics_data=analytics_data)


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        supplier_name = request.form.get('company_name')
        phone_number = request.form.get('phone_number')
        new_supplier = Supplier(company_name=supplier_name, phone_number=phone_number)
        db.session.add(new_supplier)
        db.session.commit()
        print(f"Added supplier: {supplier_name}")
        return redirect(url_for('index'))
    return render_template('add_supplier.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    locations = Location.query.all()
    if request.method == 'POST':
        location_id = int(request.form.get('location'))
        location = Location.query.filter_by(id=location_id).first()
        if not location:
            location = None
        if Users.query.filter_by(userName=request.form.get('uName')).first():
            flash("This username already exist!")
        elif Users.query.filter_by(email=request.form.get('email')).first():
            flash("You've already signed up with that email, log in instead!")
        else:
            new_user = Users(
                firstName=request.form.get('fName'),
                middleName=request.form.get('mName'),
                lastName=request.form.get('lName'),
                userName=request.form.get('uName'),
                email=request.form.get('email'),
                password=request.form.get('password'),
                location=location
            )
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully!", 'success')
        return redirect(url_for('index'))

    return render_template('add_user.html', locations=locations)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        if request.method == 'POST':
            upload = Job(
                job_title=request.form.get('job_title'),
                salary=request.form.get('salary')
            )
            db.session.add(upload)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_job.html')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    jobs = Job.query.all()
    locations = Location.query.all()

    if request.method == 'POST':
        location_id = int(request.form.get('location'))
        location = Location.query.get(location_id) if location_id != -1 else None

        job_id = int(request.form.get('job'))
        job = Job.query.get(job_id) if job_id != -1 else None

        if Employees.query.filter_by(userName=request.form.get('uName')).first():
            flash("This username already exists!", 'error')
        elif Users.query.filter_by(email=request.form.get('email')).first():
            flash("You've already signed up with that email, log in instead!", 'error')
        else:
            new_employee = Employees(
                firstName=request.form.get('fName'),
                middleName=request.form.get('mName'),
                lastName=request.form.get('lName'),
                userName=request.form.get('uName'),
                password=request.form.get('password'),
                email=request.form.get('email'),
                job=job,
                location=location
            )

            db.session.add(new_employee)
            db.session.commit()
            flash("Employee added successfully!", 'success')
        return redirect(url_for('index'))
    return render_template('add_employee.html', jobs=jobs, locations=locations)


@app.route('/<table_name>/delete/<int:item_id>', methods=['DELETE'])
def delete_item(table_name, item_id):
    if table_name == 'employees':
        item = Employees.query.get(item_id)
        if not item:
            return jsonify({'error': f'{table_name.capitalize()} not found'}), 404

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': f'{table_name.capitalize()} deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif table_name == 'users':
        item = Users.query.get(item_id)
        if not item:
            return jsonify({'error': f'{table_name.capitalize()} not found'}), 404

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': f'{table_name.capitalize()} deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif table_name == 'products':
        item = Product.query.get(item_id)
        if not item:
            return jsonify({'error': f'{table_name.capitalize()} not found'}), 404

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': f'{table_name.capitalize()} deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif table_name == 'customers':
        item = Order.query.get(item_id)
        if not item:
            return jsonify({'error': f'{table_name.capitalize()} not found'}), 404

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': f'{table_name.capitalize()} deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif table_name == 'categories':
        item = Category.query.get(item_id)
        if not item:
            return jsonify({'error': f'{table_name.capitalize()} not found'}), 404

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': f'{table_name.capitalize()} deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Table name not recognized'}), 400


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        upload = Category(
            name=request.form.get('name'),
            description=request.form.get('description')
        )
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addCategory.html')


@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        upload = Location(
            city=request.form.get('city_name'),
        )
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_location.html')

from flask import jsonify

@app.route('/mark_as_delivered/<int:order_id>', methods=['POST'])
def mark_as_delivered(order_id):
    order = Order.query.get(order_id)

    if order:
        order.delivered = True
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Order not found'}), 404



@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/view_users')
def view_users():
    users = Users.query.all()
    # Add logic to fetch and display user data
    return render_template('view_user.html', users=users)


@app.route('/view_supplier')
def view_supplier():
    suppliers = Supplier.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_supplier.html', suppliers=suppliers)


@app.route('/view_category')
def view_category():
    # Add logic to fetch and display supplier data
    categories = Category.query.all()
    return render_template('view_category.html', categories=categories)


@app.route('/view_customers')
def view_customers():
    customers = Order.query.all()
    # Add logic to fetch and display supplier dat
    return render_template('view_customers.html', customers=customers)


@app.route('/view_products')
def view_products():
    products = Product.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_products.html', products=products)


@app.route('/view_employees')
def view_employees():
    employees = Employees.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_employees.html', employees=employees)


@app.route('/view_orders')
def view_orders():
    orders = Order.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_orders.html', orders=orders)


@app.route('/view_jobs')
def view_jobs():
    jobs = Job.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_jobs.html', jobs=jobs)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    suppliers = Supplier.query.all()
    categories = Category.query.all()
    if request.method == 'POST':
        supplier_id = int(request.form.get('supplier'))
        category_id = int(request.form.get('category'))
        supplier = Supplier.query.filter_by(id=supplier_id).first()
        category = Category.query.filter_by(id=category_id).first()

        file = request.files['file']
        upload = Product(
            productName=request.form.get('productName'),
            productImg=file.read(),
            productDiscription=request.form.get('discription'),
            productPrice=request.form.get('price'),
            quantity=request.form.get('quantity'),
            category=category,
            supplier=supplier
        )
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addproduct.html', suppliers=suppliers, categories=categories)


# @app.route('/add-products', methods=['GET', 'POST'])
# def addProduct():
#     suppliers = Supplier.query.all()
#     categories = Category.query.all()
#
#     if request.method == 'POST':
#         filter_ = request.form.getlist('comp_name')
#         cat_filter = request.form.get('category')
#         print(cat_filter)
#         category = Category.query.filter(Category.name == cat_filter).first()
#
#         supplier = Supplier.query.filter(Supplier.company_name == filter_[0]).first()
#         file = request.files['file']
#         upload = Product(
#             productName=request.form.get('productName'),
#             productImg=file.read(),
#             productDiscription=request.form.get('discription'),
#             productPrice=request.form.get('price'),
#             # productCategory=request.form.get('category'),
#             category_id=category.id,
#             supplier_id=supplier.id
#         )
#         db.session.add(upload)
#         db.session.commit()
#         return render_template('addproduct.html', suppliers=suppliers, categories=categories)
#     return render_template('addproduct.html', suppliers=suppliers, categories=categories)


@app.route('/settings')
def settings():
    return render_template('settings.html')


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Logged out successfully.', 'success')
#     return redirect(url_for('index'))
# @app.route('/protected')
# @login_required
# def protected():
#     return f'Hello, {current_user.username}!'

# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         userName = request.form.get('userName')
#         password = request.form.get('password')
#         user = Users.query.filter_by(userName=userName).first()
#         category = request.form.get('category')
#         category_product = Product.query.filter(and_(Product.category == category))
#         return render_template('userInterface.html', user=user, category_product=category_product)
#     return render_template('admin.html')


@app.route('/products', methods=["GET", "POST"])
def product():
    products = Product.query.all()
    today = datetime.date.today()
    day_month_year = today.strftime("%d %B, %Y")
    if request.method == "POST":
        filter_ = request.form.get('product_selection')
        print(filter_)
        print(filter_)
        products = Product.query.filter(and_(Product.productCategory == filter_))
        products = products or 0
        print(products)
        return render_template('userInterface.html', products=products)

    return render_template('userInterface.html', products=products)


@app.template_filter('b64encode')
def b64encode_filter(s):
    if s:
        return base64.b64encode(s).decode('utf-8')
    else:
        return ""


@app.route('/add-employee', methods=['GET', 'POST'])
def addEmployee():
    jobs = Job.query.all()
    if request.method == 'POST':
        print()
        filter_ = request.form.getlist('job_title')
        job = Job.query.filter(Job.job_title == filter_[0]).first()
        print(job)
        upload = Employees(
            firstName=request.form.get('fName'),
            middleName=request.form.get('mName'),
            lastName=request.form.get('lName'),
            userName=request.form.get('uName'),
            password=request.form.get('password'),
            job_id=job.id
        )
        db.session.add(upload)
        db.session.commit()
    return render_template('addEmployee.html', jobs=jobs)


@app.route('/add-supplier', methods=['GET', 'POST'])
def addSupplier():
    if request.method == 'POST':
        upload = Supplier(
            company_name=request.form.get('company_name'),
            phone_number=request.form.get('phone_num')
        )
        db.session.add(upload)
        db.session.commit()
    return render_template('addSupplier.html')


# if __name__ == '__main__':
#     app.run(debug=True)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
