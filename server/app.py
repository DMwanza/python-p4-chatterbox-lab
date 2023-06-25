from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=['GET','POST'])
def messages():
    messages=Message.query.order_by(Message.created_at.asc()).all()
    if request.method=='GET':
        serialized_messages=[message.to_dict() for message in messages]
        response=make_response(jsonify(serialized_messages),200)
        return response

    elif request.method=='POST':
        body=request.json.get('body')
        username=request.json.get('username')
        if not body or not username:
            response_body={
                'error':'body and username invalid'
            }
            return make_response(jsonify(response_body),400)
        message=Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()),201)
@app.route('/messages/<int:id>',methods=['PATCH','DELETE'])
def messages_by_id(id):
    message=Message.query.filter_by(id=id).first()
    if request.method=='PATCH':
        for attr in request.json:
            setattr(message,attr,request.json.get(attr))
            db.session.add(message)
            db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
            )
        return response
    elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted."    
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response 

if __name__ == '__main__':
    app.run(port=5555)
