from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import uuid


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test_prep_database"
mongo = PyMongo(app)


@app.route('/')
def index():
    # Change fromdb to something more descriptive
    fromdb = mongo.db.prep.find({})
    return render_template('index.html', fromdb=fromdb)


@app.route('/add-one', methods=['GET', 'POST'])
def add_one():
    if request.method == 'POST':

        mongo.db.prep.insert_one(
            {'item': request.form['item'],
             'par': request.form['par'],
             'unit': request.form['unit'],
             'prep_time': request.form['prep_time']})
        return redirect('/')

    elif request.method == 'GET':
        return render_template('post-data.html')


@app.route('/edit-one/<id>', methods=['GET', 'POST'])
def edit_one(id=None):

    if request.method == 'GET':
        one_item = mongo.db.prep.find_one({'_id': ObjectId(id)})
        return render_template('edit-one.html', one_item=one_item)

    elif request.method == 'POST':
        button_choice = request.form['update-button']

        if button_choice == 'delete':
            mongo.db.prep.delete_one({'_id': ObjectId(request.form['id'])})
        elif button_choice == 'update':
            mongo.db.prep.update_one({'_id': ObjectId(request.form['id'])},
                                     {'$set': {'item': request.form['item'],
                                               'par': request.form['par'],
                                               'unit': request.form['unit'],
                                               'prep_time': request.form['prep_time']}}, upsert=False)

        return redirect('/')


@app.route('/inventory/', defaults={'inventory_id': None}, methods=['GET', 'POST'])
@app.route('/inventory/<inventory_id>', methods=['GET'])
def start_inventory(inventory_id):

    if request.method == 'GET':
        if inventory_id:
            print(inventory_id)

        inventory_list = mongo.db.prep.find({})
        past_inventory_lists = mongo.db.inventory_id.find({})
        date_template = {}
        for id in past_inventory_lists:
            date_template[id['inventory_id']
                          ] = id['_id'].generation_time.strftime('%A %B-%d-%Y')

        return render_template('inventory.html', inventory_list=inventory_list, date_template=date_template)
    elif request.method == 'POST':

        inventory_uuid = str(uuid.uuid1())
        doc = []
        mongo.db.inventory_id.insert_one({'inventory_id': inventory_uuid})
        for d in request.form:
            prep_item = mongo.db.prep.find_one({'_id': ObjectId(d)})
            temp = {'on_hand': request.form[d],
                    'inventory_id': inventory_uuid,
                    'item': prep_item['item']}

            doc.append(temp)
        mongo.db.inventory.insert_many(doc)

        return redirect('/inventory/')


@app.route('/show-one-inventory/<id>')
def show_one_inventory(id):
    one_inventory = mongo.db.inventory.find({'inventory_id': id})
    date_stamp = one_inventory[0]['_id'].generation_time.strftime(
        '%A %B-%d-%Y')
    print(one_inventory[0])
    return render_template('show-one-inventory.html', one_inventory=one_inventory, date_stamp=date_stamp)


@app.route('/delete-one', methods=['POST'])
def delete_one():

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
