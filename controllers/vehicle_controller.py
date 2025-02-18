from flask import render_template, request, redirect, url_for
from models.vehicle import Vehicle
from database import db

def list_vehicles():
    """Hiển thị danh sách phương tiện"""
    vehicles = Vehicle.query.all()
    return render_template('index.html', vehicles=vehicles)

def add_vehicle():
    """Thêm phương tiện mới"""
    if request.method == 'POST':
        license_plate = request.form['license_plate']
        vehicle_type = request.form['vehicle_type']
        brand = request.form['brand']
        owner = request.form['owner']
        registration_date = request.form['registration_date']

        new_vehicle = Vehicle(license_plate, vehicle_type, brand, owner, registration_date)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for('list_vehicles'))
    
    return render_template('add_vehicle.html')

def delete_vehicle(vehicle_id):
    """Xóa phương tiện"""
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
    return redirect(url_for('list_vehicles'))

def search_vehicle():
    """Tìm kiếm phương tiện"""
    keyword = request.args.get('keyword', '')
    vehicles = Vehicle.query.filter(
        (Vehicle.license_plate.contains(keyword)) |
        (Vehicle.vehicle_type.contains(keyword)) |
        (Vehicle.brand.contains(keyword)) |
        (Vehicle.owner.contains(keyword))
    ).all()
    return render_template('index.html', vehicles=vehicles)
