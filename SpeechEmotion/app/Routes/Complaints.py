from app.database import db 
from app.models import Complaints,Users
from flask import Blueprint, request,jsonify,abort


Complaints_bp = Blueprint('complaints',__name__, url_prefix='/complaints')


@Complaints_bp.route('/add_complaint/<int:user_id>', methods=['POST'])
def add_complaint(user_id):
    data = request.get_json()
    new_complaint = Complaints(
        UserID=user_id,
        Title=data['title'],
        Description=data['description'],
        Status=data.get('status', 'Open'),
        Priority=data.get('priority', 'Medium'),
        Phone=data['phone']
    )

    db.session.add(new_complaint)
    db.session.commit()
    complaint_id = new_complaint.ComplaintID
    return jsonify({'message': 'Complaint added successfully.','compiant_id':complaint_id})


@Complaints_bp.route('/getAll/<int:user_id>', methods=['GET'])
def get_complaints(user_id):
    user = Users.query.get_or_404(user_id)
    complaints = db.session.query(Complaints, Users).join(Users, Users.UserID == Complaints.UserID).filter(Complaints.UserID == user_id).all()
    
    complaints_list = [
        {
            'complaint_id': complaint.ComplaintID,
            'title': complaint.Title,
            'description': complaint.Description,
            'date_created': complaint.DateCreated,
            'status': complaint.Status,
            'priority': complaint.Priority,
            'phone': complaint.Phone,
            'first_name': user.FirstName,
            'last_name': user.LastName
        } for complaint, user in complaints
    ]
    
    return jsonify(complaints_list)

@Complaints_bp.route('/getOne/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    # Query the database to retrieve the complaint with the specified ID
    complaint = Complaints.query.get(complaint_id)

    # Check if the complaint exists
    if not complaint:
        abort(404, "Complaint not found")
    
    user = complaint.user 

    # Construct a dictionary representing the complaint data
    complaint_data = {
        'title': complaint.Title,
        'description': complaint.Description,
        'status': complaint.Status,
        'priority': complaint.Priority,
        'phone': complaint.Phone,
        'first_name': user.FirstName,
        'last_name': user.LastName
    }

    # Return the complaint data as JSON response
    return jsonify(complaint_data)



@Complaints_bp.route('/status/<int:complaint_id>', methods=['PUT'])
def close_complaint(complaint_id):
    complaint = Complaints.query.get_or_404(complaint_id)

    # Update the status of the complaint to "Closed"
    complaint.Status = 'Closed'
    db.session.commit()

    return jsonify({'message': 'Complaint closed successfully.'})


@Complaints_bp.route('/delete/<int:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    complaint = Complaints.query.get_or_404(complaint_id)

    # Check if the complaint is closed
    if complaint.Status != 'Closed':
        return jsonify({'message': 'Cannot delete complaint. It is not closed.'}), 400
    
    # Delete the complaint
    db.session.delete(complaint)
    db.session.commit()

    return jsonify({'message': 'Complaint deleted successfully.'})    