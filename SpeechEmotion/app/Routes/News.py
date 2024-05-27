from app.database import db 
from app.models import News
from flask import Blueprint, request,jsonify,abort


News_bp = Blueprint('News',__name__, url_prefix='/News')

# Define a route for inserting news for Employee
@News_bp.route('/insert_news', methods=['POST'])
def insert_news():
    data = request.get_json()  

    # Check if required fields are present
    if 'title' not in data or 'body' not in data:
        return jsonify({'error': 'Title and body are required'}), 400

    news_item = News(
        title = data['title'],
        body = data['body'],
    )    

    # Add news to the database session
    db.session.add(news_item)
    db.session.commit()

    # Return a response indicating success
    return jsonify({'message': 'News inserted successfully'})


# Define a route for retrieving all news for Client
@News_bp.route('/get_news', methods=['GET'])
def get_news():
    data = News.query.all()

    # Create a list to store news data
    news_list = []

    # Loop through each news object and extract relevant data
    for n in data:
        news_item = {
            'title': n.title,
            'body': n.body,
            'date1': n.date1.strftime("%Y-%m-%d %H:%M:%S")
        }
        news_list.append(news_item)

    # Return the list of news as JSON
    return jsonify(news_list)