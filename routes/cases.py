from flask import Blueprint, request, jsonify
from extensions.csv_manager import read_csv, append_row, generate_case_id, write_csv
from datetime import datetime
import os

cases_bp = Blueprint('cases', __name__)

@cases_bp.route('/cases/report', methods=['POST'])
def report_case():
    try:
        # Get form data
        reporter_name = request.form.get('reporter_name')
        reporter_phone = request.form.get('reporter_phone')
        location = request.form.get('location')
        animal_type = request.form.get('animal_type')
        urgency = request.form.get('urgency')
        notes = request.form.get('notes')
        
        # Handle file upload
        media_url = ''
        if 'media' in request.files:
            media_file = request.files['media']
            if media_file.filename != '':
                # Create uploads directory if it doesn't exist
                uploads_dir = 'static/uploads'
                os.makedirs(uploads_dir, exist_ok=True)
                
                # Save file with timestamp
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{media_file.filename}"
                file_path = os.path.join(uploads_dir, filename)
                media_file.save(file_path)
                media_url = f"/static/uploads/{filename}"
        
        # Generate case ID
        case_id = generate_case_id()
        
        # Create case data
        case_data = {
            'case_id': case_id,
            'reporter_name': reporter_name,
            'reporter_phone': reporter_phone,
            'location': location,
            'animal_type': animal_type,
            'urgency': urgency,
            'notes': notes,
            'media_url': media_url,
            'status': 'Reported',
            'assigned_hospital': '',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to CSV
        append_row('cases', case_data)
        
        return jsonify({
            'success': True,
            'message': f'Case reported successfully! Case ID: {case_id}',
            'case_id': case_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reporting case: {str(e)}'
        }), 500

@cases_bp.route('/cases/all', methods=['GET'])
def get_all_cases():
    try:
        df = read_csv('cases')
        cases = df.to_dict('records')
        return jsonify({
            'success': True,
            'data': cases
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching cases: {str(e)}'
        }), 500

@cases_bp.route('/cases/update-status', methods=['POST'])
def update_case_status():
    try:
        case_id = request.form.get('case_id')
        status = request.form.get('status')
        assigned_hospital = request.form.get('assigned_hospital', '')
        
        # Read current data
        df = read_csv('cases')
        
        # Find and update the case
        mask = df['case_id'] == case_id
        if not mask.any():
            return jsonify({
                'success': False,
                'message': 'Case not found'
            }), 404
            
        df.loc[mask, 'status'] = status
        if assigned_hospital:
            df.loc[mask, 'assigned_hospital'] = assigned_hospital
            
        # Save updated data
        write_csv('cases', df)
        
        return jsonify({
            'success': True,
            'message': 'Case status updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating case status: {str(e)}'
        }), 500