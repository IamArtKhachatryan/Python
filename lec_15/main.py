from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

CAR_DATABASE_FILE = 'car_inventory.json'

def ensure_database_initialized():
    if not os.path.exists(CAR_DATABASE_FILE):
        with open(CAR_DATABASE_FILE, 'w') as db_file:
            json.dump([], db_file)

def read_car_data():
    try:
        with open(CAR_DATABASE_FILE, 'r') as db_file:
            return json.load(db_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_car_data(car_data):
    with open(CAR_DATABASE_FILE, 'w') as db_file:
        json.dump(car_data, db_file, indent=4)

ensure_database_initialized()

@app.route('/cars', methods=['GET'])
def get_all_cars():
    try:
        car_inventory = read_car_data()
        return jsonify(car_inventory), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch car data', 'details': str(e)}), 500

@app.route('/cars/<int:car_id>', methods=['GET'])
def get_single_car(car_id):
    car_inventory = read_car_data()
    selected_car = next((car for car in car_inventory if car.get('id') == car_id), None)
    
    if not selected_car:
        return jsonify({'error': f'Car with ID {car_id} not found'}), 404

    return jsonify(selected_car), 200

@app.route('/cars', methods=['POST'])
def add_new_car():
    new_car_details = request.json

    if not new_car_details or 'model' not in new_car_details:
        return jsonify({'error': 'Invalid car data. "model" is required.'}), 400

    car_inventory = read_car_data()
    
    new_id = max((car.get('id', 0) for car in car_inventory), default=0) + 1
    new_car = {'id': new_id, **new_car_details}

    car_inventory.append(new_car)
    write_car_data(car_inventory)
    
    return jsonify(new_car), 201

@app.route('/cars/<int:car_id>', methods=['PUT'])
def modify_car(car_id):
    car_inventory = read_car_data()
    update_details = request.json

    car_found = False
    for car in car_inventory:
        if car.get('id') == car_id:
            car.update(update_details)
            car_found = True
            break

    if not car_found:
        return jsonify({'error': f'Car with ID {car_id} not found'}), 404

    write_car_data(car_inventory)
    return jsonify({'message': 'Car updated successfully', 'car': car}), 200

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def remove_car(car_id):
    car_inventory = read_car_data()
    filtered_inventory = [car for car in car_inventory if car.get('id') != car_id]

    if len(car_inventory) == len(filtered_inventory):
        return jsonify({'error': f'Car with ID {car_id} not found'}), 404

    write_car_data(filtered_inventory)
    return jsonify({'message': f'Car with ID {car_id} deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
