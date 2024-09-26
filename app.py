from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

# 환경 변수에서 MongoDB URI 가져오기
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# 기본 루트 추가 (앱 동작 확인용)
@app.route('/')
def index():
    return render_template('index.html')

# 인스타그램 ID를 저장하는 API
@app.route('/save_instagram_id', methods=['POST'])
def save_instagram_id():
    data = request.json
    user_instagram_id = data.get('userInstagramID')
    target_instagram_id = data.get('targetInstagramID')

    if not user_instagram_id or not target_instagram_id:
        return jsonify({"error": "Instagram ID is required"}), 400

    # 중복 확인
    existing_entry = mongo.db.instagram_ids.find_one({
        'user_instagram_id': user_instagram_id,
        'target_instagram_id': target_instagram_id
    })

    if existing_entry:
        return jsonify({"error": "This Instagram ID pair already exists."}), 409

    # MongoDB에 데이터 저장
    mongo.db.instagram_ids.insert_one({
        'user_instagram_id': user_instagram_id,
        'target_instagram_id': target_instagram_id
    })

    return jsonify({"message": "IDs saved successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
