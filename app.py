from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///iFleet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app) 
migrate = Migrate(app, db)
ma = Marshmallow(app)

class customers(db.Model):
    __tablename__ = 'customers' 
    customerid = db.Column('customerid', db.Integer, primary_key=True, autoincrement=True, unique=True)
    customerName = db.Column('customerName', db.Text)
    address = db.Column('address', db.Text)
    spoc = db.Column('spoc', db.Integer)
    phone = db.Column('phone', db.Integer)
    email = db.Column('email', db.Text)
    gst = db.Column('gst', db.Text)
    tenetid = db.Column('tenetid', db.Text)
    cloudUserName = db.Column('cloudUserName', db.Text)
    cloudPassword = db.Column('cloudPassword', db.Text)


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = customers

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#Routes

@app.route('/')
def hello():
   return 'Hello'

#API ROUTE TO ADD CUSTOMER
@app.route('/addcustomers', methods=['POST'])
def add_customer():
    customer_data = request.json
    new_customer = customers(**customer_data)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

#API ROUTE TO DISPLAY SINGLE CUSTOMER 
@app.route('/getcustomers/<id>', methods=['GET'])
def get_customer(id):
    customer = customers.query.get(id)
    return customer_schema.jsonify(customer)

#API ROUTE TO DISPLAY ALL CUSTOMERS 
@app.route('/getcustomers', methods=['GET'])
def get_all_customers():
    all_customers = customers.query.all()
    return customers_schema.jsonify(all_customers)

#API ROUTE TO DELETE CUSTOMER BY ID 
@app.route('/delcustomers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = customers.query.get(id)

    if customer:
        db.session.delete(customer)
        db.session.commit()

        return customer_schema.jsonify(customer)
    else:
        return jsonify({'message': 'Customer not found'}), 404

#API ROUTE TO UPDATE CUSTOMER BY ID 
@app.route('/updatecustomers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = customers.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200


if __name__ == '__main__':
   app.run(debug = True)
