from app.database import db 
from app.models import News
from flask import Blueprint, request,jsonify,abort


News_bp = Blueprint('News',__name__, url_prefix='/News')

# Define a route for inserting news for Employee , UserID here is the employee
@News_bp.route('/insert_news/<int:UserID>', methods=['POST'])
def insert_news(UserID):
    data = request.get_json()  


    if 'title' not in data or 'body' not in data:
        return jsonify({'error': 'Title and body are required'}), 400

    news_item = News(
        title=data['title'],
        body=data['body'],
        UserID=UserID,
    )  
    db.session.add(news_item)
    db.session.commit()


    return jsonify({'message': 'News inserted successfully', 'newsID': news_item.newsID})


# Define a route for retrieving all news for Client
@News_bp.route('/get_news', methods=['GET'])
def get_news():
    data = News.query.all()

    news_list = []

    for n in data:
        news_item = {
            'title': n.title,
            'body': n.body,
            'date1': n.date1.strftime("%Y-%m-%d %H:%M:%S")
        }
        news_list.append(news_item)

    return jsonify(news_list)


@News_bp.route('/update_news/<int:newsID>', methods=['PUT'])
def update_news(newsID):
    data = request.get_json()

    news_item = News.query.get(newsID)
    
    if news_item is None:
        return jsonify({'error': 'News item not found'}), 404

    if 'title' in data:
        news_item.title = data['title']
    if 'body' in data:
        news_item.body = data['body']

    db.session.commit()

    return jsonify({'message': 'News updated successfully'})


@News_bp.route('/delete_news/<int:newsID>', methods=['DELETE'])
def delete_news(newsID):
    news_item = News.query.get(newsID)

    if news_item is None:
        return jsonify({'error': 'News item not found'}), 404
    db.session.delete(news_item)
    db.session.commit()

    return jsonify({'message': 'News deleted successfully'})