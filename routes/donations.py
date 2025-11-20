from flask import Blueprint, request, jsonify
from extensions.csv_manager import read_csv, append_row
from datetime import datetime
import pandas as pd
import numpy as np

donations_bp = Blueprint('donations', __name__)

@donations_bp.route('/donations/add', methods=['POST'])
def add_donation():
    try:
        # Get form data
        donor_name = request.form.get('donor_name')
        donor_email = request.form.get('donor_email')
        amount = request.form.get('amount')
        category = request.form.get('category')
        
        # Create donation data
        donation_data = {
            'donor_name': donor_name,
            'donor_email': donor_email,
            'amount': amount,
            'category': category,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to CSV
        append_row('donations', donation_data)
        
        return jsonify({
            'success': True,
            'message': 'Donation recorded successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error recording donation: {str(e)}'
        }), 500

@donations_bp.route('/donations/all', methods=['GET'])
def get_all_donations():
    try:
        df = read_csv('donations')
        # Sanitize DataFrame to ensure JSON serializable data
        if not df.empty:
            df = df.fillna('')
            df = df.replace({np.nan: '', pd.NaT: ''})
            # Convert all columns to string to ensure JSON serializable
            for col in df.columns:
                df[col] = df[col].astype(str)
        donations = df.to_dict('records')
        return jsonify({
            'success': True,
            'data': donations
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching donations: {str(e)}'
        }), 500