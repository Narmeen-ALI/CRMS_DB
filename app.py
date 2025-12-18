from flask import Flask, request, jsonify, send_file,send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from generate_pdf import create_pdf_report

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'iamnarmeen'),
    'database': os.getenv('DB_NAME', 'crime_reports')
}

STATUS_OPTIONS = ['Filed', 'Investigating', 'Closed']

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def clean_input(key, data, default=''):
    """Clean and extract input from request data"""
    return data.get(key, default).strip() if isinstance(data.get(key), str) else default


@app.route('/api', methods=['GET', 'POST'])
def api():
    """Main API endpoint handling all CRUD operations for reports"""
    action = request.args.get('action', 'read')
    
    if request.method == 'POST':
        body = request.get_json() or {}
    else:
        body = {}
    
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        if action == 'create':
            reporter = clean_input('reporter', body)
            suspect = clean_input('suspect', body)
            crime = clean_input('crime', body)
            location = clean_input('location', body)
            
            if not all([reporter, suspect, crime, location]):
                return jsonify({'error': 'Missing required fields'}), 422
            
            status_value = clean_input('status', body, 'Filed')
            if status_value not in STATUS_OPTIONS:
                status_value = 'Filed'
            
            notes = clean_input('notes', body)
            
            cursor = db.cursor()
            query = """
                INSERT INTO reports (reporter, suspect, crime, status, location, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (reporter, suspect, crime, status_value, location, notes))
            db.commit()
            report_id = cursor.lastrowid
            cursor.close()
            
            return jsonify({'message': 'Report added', 'id': report_id}), 201
        
        elif action == 'update':
            if not body.get('id'):
                return jsonify({'error': 'Missing record id'}), 422
            
            reporter = clean_input('reporter', body)
            suspect = clean_input('suspect', body)
            crime = clean_input('crime', body)
            location = clean_input('location', body)
            
            if not all([reporter, suspect, crime, location]):
                return jsonify({'error': 'Missing required fields'}), 422
            
            status_value = clean_input('status', body, 'Filed')
            if status_value not in STATUS_OPTIONS:
                status_value = 'Filed'
            
            notes = clean_input('notes', body)
            report_id = body['id']
            
            cursor = db.cursor()
            query = """
                UPDATE reports 
                SET reporter=%s, suspect=%s, crime=%s, status=%s, location=%s, notes=%s
                WHERE id=%s
            """
            cursor.execute(query, (reporter, suspect, crime, status_value, location, notes, report_id))
            db.commit()
            cursor.close()
            
            return jsonify({'message': 'Report updated'}), 200
        
        elif action == 'delete':
            if not body.get('id'):
                return jsonify({'error': 'Missing record id'}), 422
            
            report_id = body['id']
            cursor = db.cursor()
            query = "DELETE FROM reports WHERE id=%s"
            cursor.execute(query, (report_id,))
            db.commit()
            cursor.close()
            
            return jsonify({'message': 'Report deleted'}), 200
        
        else:  # read
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT id, reporter, suspect, crime, status, location, notes, created_at
                FROM reports
                ORDER BY id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                if row.get('created_at') and isinstance(row['created_at'], datetime):
                    row['created_at'] = row['created_at'].isoformat()
        
            return jsonify({'data': rows}), 200
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if db.is_connected():
            db.close()
#-----------------------------------------------


@app.route('/api/categories', methods=['GET', 'POST', 'PUT', 'DELETE'])
def categories_api():
    """API for managing crime categories"""
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        if request.method == 'GET':
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM crime_categories ORDER BY id DESC"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                if row.get('created_at'):
                    row['created_at'] = row['created_at'].isoformat()
            
            return jsonify({'data': rows}), 200
        
        elif request.method == 'POST':
            body = request.get_json()
            cursor = db.cursor()
            query = """
                INSERT INTO crime_categories (category_name, severity, description, typical_punishment)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                body['category_name'], body['severity'], 
                body['description'], body.get('typical_punishment')
            ))
            db.commit()
            category_id = cursor.lastrowid
            cursor.close()
            return jsonify({'message': 'Category added', 'id': category_id}), 201
        
        elif request.method == 'PUT':
            body = request.get_json()
            cursor = db.cursor()
            query = """
                UPDATE crime_categories 
                SET category_name=%s, severity=%s, description=%s, typical_punishment=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                body['category_name'], body['severity'], 
                body['description'], body.get('typical_punishment'), body['id']
            ))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Category updated'}), 200
        
        elif request.method == 'DELETE':
            body = request.get_json()
            cursor = db.cursor()
            query = "DELETE FROM crime_categories WHERE id=%s"
            cursor.execute(query, (body['id'],))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Category deleted'}), 200
    
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.is_connected():
            db.close()


@app.route('/api/officers', methods=['GET', 'POST', 'PUT', 'DELETE'])
def officers_api():
    """API for managing officers"""
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        if request.method == 'GET':
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM officers ORDER BY id DESC"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                if row.get('created_at'):
                    row['created_at'] = row['created_at'].isoformat()
                if row.get('join_date'):
                    row['join_date'] = row['join_date'].isoformat()
            
            return jsonify({'data': rows}), 200
        
        elif request.method == 'POST':
            body = request.get_json()
            cursor = db.cursor()
            query = """
                INSERT INTO officers (badge_number, full_name, officer_rank, department, phone, email, station, join_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                body['badge_number'], body['full_name'], body['officer_rank'],
                body['department'], body.get('phone'), body.get('email'),
                body.get('station'), body.get('join_date')
            ))
            db.commit()
            officer_id = cursor.lastrowid
            cursor.close()
            return jsonify({'message': 'Officer added', 'id': officer_id}), 201
        
        elif request.method == 'PUT':
            body = request.get_json()
            cursor = db.cursor()
            query = """
                UPDATE officers 
                SET badge_number=%s, full_name=%s, officer_rank=%s, department=%s, 
                    phone=%s, email=%s, station=%s, join_date=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                body['badge_number'], body['full_name'], body['officer_rank'],
                body['department'], body.get('phone'), body.get('email'),
                body.get('station'), body.get('join_date'), body['id']
            ))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Officer updated'}), 200
        
        elif request.method == 'DELETE':
            body = request.get_json()
            cursor = db.cursor()
            query = "DELETE FROM officers WHERE id=%s"
            cursor.execute(query, (body['id'],))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Officer deleted'}), 200
    
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.is_connected():
            db.close()



@app.route('/api/suspects', methods=['GET', 'POST', 'PUT', 'DELETE'])
def suspects_api():
    """API for managing suspects"""
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        if request.method == 'GET':
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM suspects ORDER BY id DESC"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                if row.get('created_at'):
                    row['created_at'] = row['created_at'].isoformat()
            
            return jsonify({'data': rows}), 200
        
        elif request.method == 'POST':
            body = request.get_json()
            cursor = db.cursor()
            query = """
                INSERT INTO suspects (full_name, alias, age, gender, address, phone, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                body['full_name'], 
                body.get('alias'), 
                body.get('age'),
                body.get('gender'), 
                body.get('address'), 
                body.get('phone'),
                body.get('status', 'At Large') 
            ))
            db.commit()
            suspect_id = cursor.lastrowid
            cursor.close()
            return jsonify({'message': 'Suspect added', 'id': suspect_id}), 201
        
        elif request.method == 'PUT':
            body = request.get_json()
            cursor = db.cursor()
            query = """
                UPDATE suspects 
                SET full_name=%s, alias=%s, age=%s, gender=%s, 
                    address=%s, phone=%s, status=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                body['full_name'], 
                body.get('alias'), 
                body.get('age'),
                body.get('gender'), 
                body.get('address'), 
                body.get('phone'),
                body.get('status'), 
                body['id']
            ))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Suspect updated'}), 200
        
        elif request.method == 'DELETE':
            body = request.get_json()
            cursor = db.cursor()
            query = "DELETE FROM suspects WHERE id=%s"
            cursor.execute(query, (body['id'],))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Suspect deleted'}), 200
    
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.is_connected():
            db.close()



@app.route('/api/evidence', methods=['GET', 'POST', 'PUT', 'DELETE'])
def evidence_api():
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        if request.method == 'GET':
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM evidence ORDER BY id ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                if row.get('created_at'): row['created_at'] = row['created_at'].isoformat()
                if row.get('collection_date'): row['collection_date'] = row['collection_date'].isoformat()
            
            return jsonify({'data': rows}), 200
        
        elif request.method == 'POST':
            body = request.get_json()
            cursor = db.cursor()
            # UPDATED: Added evidence_number, case_number, storage_location, chain_of_custody
            query = """
                INSERT INTO evidence (report_id, evidence_type, description, collected_by, 
                                    collection_date, location_found, evidence_number, 
                                    case_number, storage_location, chain_of_custody)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                body['report_id'], body['evidence_type'], body['description'],
                body.get('collected_by'), body.get('collection_date'), body.get('location_found'),
                body.get('evidence_number'), body.get('case_number'), 
                body.get('storage_location'), body.get('chain_of_custody')
            ))
            db.commit()
            evidence_id = cursor.lastrowid
            cursor.close()
            return jsonify({'message': 'Evidence added', 'id': evidence_id}), 201
        
        elif request.method == 'PUT':
            body = request.get_json()
            cursor = db.cursor()
            # UPDATED: Added all new columns to UPDATE query
            query = """
                UPDATE evidence 
                SET report_id=%s, evidence_type=%s, description=%s, 
                    collected_by=%s, collection_date=%s, location_found=%s,
                    evidence_number=%s, case_number=%s, storage_location=%s, 
                    chain_of_custody=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                body['report_id'], body['evidence_type'], body['description'],
                body.get('collected_by'), body.get('collection_date'), 
                body.get('location_found'), body.get('evidence_number'),
                body.get('case_number'), body.get('storage_location'), 
                body.get('chain_of_custody'), body['id']
            ))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Evidence updated'}), 200
        
  
        #----------------------------------------------
        elif request.method == 'DELETE':
            body = request.get_json()
            cursor = db.cursor()
            query = "DELETE FROM evidence WHERE id=%s"
            cursor.execute(query, (body['id'],))
            db.commit()
            cursor.close()
            return jsonify({'message': 'Evidence deleted'}), 200
    
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db.is_connected():
            db.close()



@app.route('/api/download-pdf/<int:report_id>', methods=['GET'])
def download_pdf(report_id):
    """Generate comprehensive PDF with report, evidence, suspects, and officers"""
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = db.cursor(dictionary=True)
        

        query = "SELECT * FROM reports WHERE id=%s"
        cursor.execute(query, (report_id,))
        report = cursor.fetchone()
        
        if not report:
            cursor.close()
            return jsonify({'error': 'Report not found'}), 404
        
       
        if report.get('created_at'):
            report['created_at'] = report['created_at'].strftime('%B %d, %Y %I:%M %p')
        
        
        query = "SELECT * FROM evidence WHERE report_id=%s"
        cursor.execute(query, (report_id,))
        evidence_list = cursor.fetchall()
        
    
        for ev in evidence_list:
            if ev.get('collection_date'):
                ev['collection_date'] = ev['collection_date'].strftime('%Y-%m-%d')
        
   
        suspect_name = report.get('suspect', '')
        suspects_list = []
        if suspect_name and suspect_name.lower() != 'unknown':
            query = "SELECT * FROM suspects WHERE full_name LIKE %s"
            cursor.execute(query, (f"%{suspect_name}%",))
            suspects_list = cursor.fetchall()
      

        query = "SELECT * FROM officers WHERE officer_status='Active' LIMIT 3"
        cursor.execute(query)
        officers_list = cursor.fetchall()
        
        cursor.close()
        
 
        filename = create_pdf_report(
            report_data=report,
            evidence_list=evidence_list,
            suspects_list=suspects_list,
            officers_list=officers_list
        )
        
        return send_file(
            filename,
            as_attachment=True,
            download_name=f"Crime_Report_{report_id}_Complete.pdf",
            mimetype='application/pdf'
        )
    
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500
    finally:
        if db.is_connected():
            db.close()


@app.route('/')
def index():
    """Healthy check endpoint"""
    return jsonify({'status': 'ok', 'message': 'CRMS API is running'}), 200
# Static files serve karne ke liye
@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    