from flask import Blueprint, render_template, jsonify

common_bp = Blueprint('common', __name__)

@common_bp.route('/')
def index():
    return render_template('index.html')

@common_bp.route('/report-case')
def report_case_page():
    return render_template('report_case.html')

@common_bp.route('/donate')
def donate_page():
    return render_template('donate.html')

@common_bp.route('/hospitals')
def hospitals_page():
    return render_template('hospitals.html')

@common_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'ResQTrack is running properly'
    }), 200