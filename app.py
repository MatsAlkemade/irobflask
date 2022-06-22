from flask import Flask,jsonify,redirect,render_template,request,redirect,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
# import static.py.main as main
# import static.py.refreshImg as refreshImg


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productcode = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone("Europe/Amsterdam")))

    def __repr__(self):
        return '<Product %r>' % self.id
    
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(200))
    accuracy = db.Column(db.Integer)
    barcode = db.Column(db.String(200))
    date_created = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Match %r>' % self.id

@app.route('/', methods=['GET'])
def index():
    products = Product.query.order_by(Product.date_created).all()
    return render_template('index.html', products=products)

@app.route('/scanner', methods=['POST', 'GET'])
def scanner():
    if request.method == 'POST':
        productcode = request.form['productcode']
        product_name = request.form['product_name']
        new_product = Product(productcode=productcode, product_name=product_name)
        try:
            db.session.add(new_product)
            db.session.commit()
            return jsonify({
                'id' : new_product.id,
                'productcode' : new_product.productcode,
                'product_name' : new_product.product_name,
                'date_created' : new_product.date_created.strftime("%Y") + "-" + new_product.date_created.strftime("%m") + "-" + new_product.date_created.strftime("%d")
            })
               
        except:
            return "Er is iets fout gegaan"
    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template('scanner.html', products=products)

@app.route('/producten', methods=['GET'])
def products():
    matches = Match.query.order_by(Match.date_created).all()
    return render_template('products.html', matches=matches)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    product_to_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return jsonify({
            'id' : id
        })
    except:
        return 'Er is iets foutgegaan'

@app.route('/python', methods=["POST"])
def python():
    # roep main.py aan
    return "Success"

# app.route('/refreshimg', methods=["POST"])
# def refreshimg():
#     return refreshImg.refreshImg()
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)

