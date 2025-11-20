from flask import Blueprint, request, jsonify
from extensions.csv_manager import read_csv, append_row
from datetime import datetime
import requests

hospitals_bp = Blueprint('hospitals', __name__)

@hospitals_bp.route('/hospitals/search', methods=['GET'])
def search_hospitals():
    try:
        city = request.args.get('city')
        if not city:
            return jsonify({
                'success': False,
                'message': 'City parameter is required'
            }), 400
        
        # Call OpenStreetMap Nominatim API
        url = f"https://nominatim.openstreetmap.org/search?format=json&q=hospital in {city}"
        headers = {
            'User-Agent': 'ResQTrack/1.0 (Animal Rescue Coordination Platform)'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Filter and format results
        hospitals = []
        for item in data:
            hospitals.append({
                'name': item.get('display_name', '').split(',')[0],
                'address': item.get('display_name', ''),
                'lat': item.get('lat', ''),
                'lon': item.get('lon', ''),
                'boundingbox': item.get('boundingbox', [])
            })
        
        return jsonify({
            'success': True,
            'data': hospitals
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error searching hospitals: {str(e)}'
        }), 500

@hospitals_bp.route('/hospitals/add', methods=['POST'])
def add_hospital():
    try:
        # Get form data
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone', '')
        location = request.form.get('location')
        api_lat = request.form.get('api_lat', '')
        api_lon = request.form.get('api_lon', '')
        
        # Create hospital data
        hospital_data = {
            'name': name,
            'address': address,
            'phone': phone,
            'location': location,
            'api_lat': api_lat,
            'api_lon': api_lon,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to CSV
        append_row('hospitals', hospital_data)
        
        return jsonify({
            'success': True,
            'message': 'Hospital added successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding hospital: {str(e)}'
        }), 500

@hospitals_bp.route('/hospitals/all', methods=['GET'])
def get_all_hospitals():
    try:
        df = read_csv('hospitals')
        hospitals = df.to_dict('records')
        return jsonify({
            'success': True,
            'data': hospitals
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching hospitals: {str(e)}'
        }), 500