from flask import Blueprint, request, jsonify, render_template
from extensions.csv_manager import read_csv, write_csv, append_row
from datetime import datetime
import pandas as pd
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

@admin_bp.route('/admin/table/<table_name>')
def admin_table(table_name):
    try:
        # Validate table name
        valid_tables = ['cases', 'donations', 'hospitals', 'emergency']
        if table_name not in valid_tables:
            return jsonify({
                'success': False,
                'message': 'Invalid table name'
            }), 400
        
        # Read data
        df = read_csv(table_name)
        data = df.to_dict('records')
        
        # Return JSON data for AJAX requests
        if request.args.get('format') == 'json':
            return jsonify({
                'success': True,
                'data': data
            }), 200
        
        # For now, just return JSON (will implement HTML rendering later)
        return jsonify({
            'success': True,
            'data': data,
            'table': table_name
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching table data: {str(e)}'
        }), 500

@admin_bp.route('/admin/api/<table_name>', methods=['GET', 'POST'])
def admin_api(table_name):
    try:
        # Validate table name
        valid_tables = ['cases', 'donations', 'hospitals', 'emergency']
        if table_name not in valid_tables:
            return jsonify({
                'success': False,
                'message': 'Invalid table name'
            }), 400
        
        if request.method == 'GET':
            # Return all records
            df = read_csv(table_name)
            data = df.to_dict('records')
            return jsonify({
                'success': True,
                'data': data
            }), 200
            
        elif request.method == 'POST':
            # Handle different actions
            action = request.form.get('action')
            
            if action == 'delete':
                # Delete a record by index or ID
                record_id = request.form.get('id')
                df = read_csv(table_name)
                
                # For cases, use case_id; for others, we might need to use index
                if table_name == 'cases':
                    df = df[df['case_id'] != record_id]
                else:
                    # For simplicity, we'll skip delete for other tables in this implementation
                    return jsonify({
                        'success': False,
                        'message': 'Delete action not implemented for this table'
                    }), 400
                
                write_csv(table_name, df)
                return jsonify({
                    'success': True,
                    'message': 'Record deleted successfully'
                }), 200
                
            elif action == 'add':
                # Add a new record
                data = request.form.to_dict()
                # Remove the 'action' key
                data.pop('action', None)
                # Add timestamp
                data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                append_row(table_name, data)
                return jsonify({
                    'success': True,
                    'message': 'Record added successfully'
                }), 200
                
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid action'
                }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing request: {str(e)}'
        }), 500

@admin_bp.route('/admin/stats')
def admin_stats():
    try:
        # Get counts for each table
        cases_df = read_csv('cases')
        donations_df = read_csv('donations')
        hospitals_df = read_csv('hospitals')
        
        # Calculate statistics
        total_cases = len(cases_df)
        total_donations = len(donations_df)
        total_hospitals = len(hospitals_df)
        
        # Calculate total donation amount
        total_amount = 0
        if not donations_df.empty and 'amount' in donations_df.columns:
            # Convert amount column to numeric, handling any non-numeric values
            donations_df['amount'] = pd.to_numeric(donations_df['amount'], errors='coerce')
            total_amount = donations_df['amount'].sum()
        
        return jsonify({
            'success': True,
            'data': {
                'total_cases': total_cases,
                'total_donations': total_donations,
                'total_hospitals': total_hospitals,
                'total_amount': float(total_amount)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching statistics: {str(e)}'
        }), 500