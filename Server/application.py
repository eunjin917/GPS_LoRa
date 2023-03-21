from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pytz import timezone
import pymysql  # pip install pymysql

app = Flask(__name__)

KST = timezone("Asia/Seoul")





# 인덱스 페이지
@app.route('/')
def index_page():
    return "<h1>최은진 졸업과제 - Flask 서버</h1>"


# DB 저장 페이지
@app.route('/receivepage', methods=['POST'])
def receivepage():
    if request.method == "POST":
        # 위도/경도 json 받아오기
        jsonreq = request.form.get("info")
        
        # 데이터 파싱
        val = jsonreq.split('/')
        val[1] = datetime.now(KST).strftime("%Y-%m-%dT%H:%M:00") # 날짜, 시간 넣기
        val[2] = int(val[2][:2]) + float(val[2][2:])/60    # 위도 : ddmm.mmmm -> dd+(mm.mmmm/60)
        val[3] = int(val[3][:3]) + float(val[3][3:])/60    # 경도 : dddmm.mmmm -> ddd+(mm.mmmm/60)
        
        val[2] = str(val[2])
        val[3] = str(val[3])
        
        db = pymysql.connect(
            host='localhost',
            user='root',
            database='gps',
        )
        cursor = db.cursor()
        
        # DB insert
        sql = "INSERT INTO info (time, latitude, longitude) VALUES (%s, %s, %s);"
        # try:
        cursor.execute(sql, val[1:4])
        db.commit()
        print("DB insert : ", end='')
        print(val[1:4])
        db.close()


        
        return ""


# DB 확인 페이지
@app.route('/dbprintpage')
def dbprintpage():
    db = pymysql.connect(
        host='localhost',
        user='root',
        database='gps',
    )
    cursor = db.cursor()

    sql = "SELECT * FROM info;"
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()

    return render_template("dbprintpage.html", result=result)


# 카카오i오픈빌더 연결하는 페이지
@app.route('/postpage', methods=['POST'])
def postpage():
    if request.method == "POST":
        # 사용자가 입력한 시간/날짜 json 받아오기
        jsonreq = request.get_json()
        inputtime = jsonreq["action"]["detailParams"]["datetime"]["origin"]

        db = pymysql.connect(
            host='localhost',
            user='root',
            database='gps',
        )
        cursor = db.cursor()
        
        # DB에서 위도/경도 찾기 - 해당 시간 기준 최신 record 불러옴
        sql = "SELECT * FROM info WHERE time <= '" + inputtime + "' ORDER BY time DESC;"
        cursor.execute(sql)
        result = cursor.fetchone()
        time = result[0]
        lantitude = result[1]
        longitude = result[2]
        
        # 카카오맵 지도 이미지 불러오기
        # url = "https://eunjin917-mscvd.run.goorm.io/kakaomap/" + time + '/' + lantitude + '/'+longitude
        kakaomapUrl = "https://map.kakao.com/link/map/" + time + "," + lantitude + "," + longitude
        print("카카오맵 : " + kakaomapUrl)
        
        # 위치 정보 json 보내기
        res = {
          "contents":[
            {
              "type":"card.image",
              "cards":[
                {
                  "imageUrl":"https://w.namu.la/s/9b7194fc88bd6c36c484273bf153f116e47df16d8112691483123c8832bd9f7203a2964ad8f2293fe540e5c939f917d6084b3b7c23aad1c5523e4198ba7d317aa5d18f9aad63e7716c7b547fba411204",
                  "description":"선택한 날짜/시간 기준 최신 위치입니다. 자세한 위치를 확인하려면 아래 버튼을 클릭하세요.",
                  "title":time+" 위치",
                  "buttons":[
                    {
                      "type":"url",
                      "label":"카카오맵 바로가기",
                      "data":{
                          "url":kakaomapUrl
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
        return jsonify(res)

    
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)