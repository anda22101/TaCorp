from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone
from myapp import db
from sqlalchemy import Enum


db = SQLAlchemy()


## User related models ##


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    
    role = db.Column(
        Enum('admin', 'employee', 'general_user', name='user_roles'),
        nullable=False,
        default='general_user'
    )

    payment_method = db.Column(
        Enum('cash', 'sll', 'card', name='payment_methods'),
        nullable=False,
        default='cash'
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(tz=timezone.utc), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
## User related models ##




## Product related models ##
class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=False)
    weight_capacity = db.Column(db.Float, nullable=False)
    body_type = db.Column(
        Enum('MS', 'SS', 'ABS', 'NORMAL', name='body_material'),
        nullable=False,
        default='NORMAL'
    )
    category = db.Column(
        Enum('PLATFORM', 'BENCH SCALE', 'NORMAL', name='product_type'),
        nullable=False,
        default='NORMAL'
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(tz=timezone.utc), nullable=True)
    product_picture = db.Column(db.String(200), nullable=True)


class Promotion(db.Model):
    __tablename__ = 'promotions'
    promotion_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
## Product related models ##



## Review related models ##
class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc), nullable=False)
    product_picture = db.Column(db.String(200), nullable=True)
## Review related models ##   

## order related models ##  
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_status = db.Column(
        Enum('Pending', 'Confirmed', 'Delivered', name='order_status'),
        nullable=False,
        default='NORMAL'
    )
    payment_status = db.Column(
        Enum('Pending', 'Completed' , name='payment_status'),
        nullable=False,
        default='Pending'
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(tz=timezone.utc), nullable=True)


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.coupon_id'), nullable=True)
 

class Cart(db.Model):
    __tablename__ = 'carts'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Coupon(db.Model):
    __tablename__ = 'coupons'
    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=True)


class Shipping(db.Model):
    __tablename__ = 'shipping'
    shipping_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    shipping_cost = db.Column(db.Float, nullable=False)
    tracking_number = db.Column(db.String(50), nullable=False)
## order related models ## 




## Admin privilege related models ## 
class AdminAction(db.Model):
    __tablename__ = 'admin_actions'
    admin_action_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action_area = db.Column(
        Enum('Order', 'User', 'Product', 'Employee', 'Complaint' , name='Action_Area'),
        nullable=False,
        default='None'
    )
    action_type = db.Column(
        Enum('Viewed', "Not Viewed", 'Deleted', 'Modified', 'Completed' , name='Action_Taken'),
        nullable=False,
        default='Not Viewed'
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(tz=timezone.utc), nullable=True)
## Admin privilege related models ##




## Contact related models ##
class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'
    inquiry_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=timezone.utc), nullable=False)
## Contact related models ##   








