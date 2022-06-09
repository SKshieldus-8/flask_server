from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timedelta
from detectionwork import GtnOcr


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'





@app.route("/login", methods=['POST'])
def login():
    userinfo = request.json
    user = User.query.first()
    userid = userinfo['name']
    password = userinfo['password']
    
    if user.name == userid and user.password == password:
        return jsonify("Access_token")
    else:
        return 'id/password is wrong', 401
    
    
@app.route('/decryption', methods=['POST', 'GET'])
def get_key():
    pass
#    auth_token = request.get_json()
#    # 인증 성공 - 토큰 일치
#    if auth_token.get('access_token') == GtnServer.access_token:
#        return jsonify({
#            "result": 1,
#            "decry_key": GtnServer.decry_key
#        })
#    # 인증 실패 - 토큰 불일치
#    else:
#        return {
#            "result": 0,
#            "msg": "권한이 없는 요청입니다."
#        }, 401

# OCR API


@app.route('/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        # 파일이 첨부되어 있는가 확인
        if 'file' not in request.files:
            return jsonify({
                "result": 0,
                "msg": "파일이 없습니다."
            })

        file = request.files['file']

        if file and GtnOcr.allowed_file(file.filename):
            # 검증에 필요한 자료구조 및 변수
            coordinate = dict()
            verif_idcard = list(0 for i in range(0, 5))
            verif_license = list(0 for i in range(0, 5))
            verif_regist = list(0 for i in range(0, 9))
            jumin_cnt = 0
            license_cnt = 0

            parsed = GtnOcr.reader.readtext(file.read())
            contents = GtnOcr.get_coordinate(
                parsed, coordinate, verif_idcard, verif_license, verif_regist, jumin_cnt, license_cnt)
            # 개인정보 탐지 내용이 없을 경우
            if contents == {}:
                return jsonify({
                    "result": 0,
                    "msg": "No Contents"
                })
            # 개인정보 탐지 내용이 있을 경우
            else:
                # return jsonify(contents)
                # return json.dumps(contents, ensure_ascii=False, sort_keys=True)
                # body = json.dumps(contents, ensure_ascii=False, sort_keys=True)
                # return body
                return {
                    "result": 1,
                    "data": contents
                }
        # 파일 형식이 허용되지 않을 경우
        else:
            return jsonify({
                "result": 0,
                "msg": "허용되지 않는 파일 형식입니다."
            }), 403
    # POST 의외의 방식 방지
    else:
        return jsonify({
            "result": 0,
            "msg": "허용되지 않은 접근입니다."
        }), 403