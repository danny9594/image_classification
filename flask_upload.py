import classifier
import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

color_path = './static/voice_clothes/color/'
cloth_path = './static/voice_clothes/cloth/'
color_list = ['beige', 'black', 'brown', 'gray', 'green', 'navy', 'red', 'white']
color_list_kor = ['베이지색','검정색','갈색','회색','초록색','네이비색','빨간색','하얀색']
cloth_list = ['top', 'bottom', 'etc']
cloth_list_kor = ['상의', '하의', '기타']

# upload html rendering
@app.route('/')
def render_file():
    return render_template('A-eye.html')

# file upload 처리
@app.route('/fileUpload_old', methods=['GET','POST'])
def upload_file():
    # file을 classifier를 사용하여 판별
    f = request.files['file']
    color = classifier.class_color(f)
    cloth = classifier.class_cloth(f)

    # mp3 path 설정
    mp3_path_color = color_path + color_list[color] + '.mp3'
    mp3_path_cloth = cloth_path + cloth_list[cloth] + '.mp3'

    # 판별한 값 문자열로 변경
    color = color_list_kor[color]
    cloth = cloth_list_kor[cloth]

    classifi_result = '이 옷의 색상은 ' + color + '이며<br>' + cloth + '로 판별되었습니다.'

    # html 불러오기
    h = open('./static/upload_top.txt')
    html_top = h.read()
    h = open('./static/upload_bottom.txt')
    html_bottom = h.read()

    # 작동하는 코드 
    # temp = """<audio autoplay controls> <source src= "./static/voice_clothes/color/beige.mp3" type="audio/mp3"> </audio>"""

    voice_color = """<audio autoplay controls> <source src= """ + '"' + mp3_path_color + '"' +  """ type="audio/mp3"> </audio>"""
    voice_cloth = """<audio autoplay controls> <source src= """ + '"' + mp3_path_cloth + '"' +  """ type="audio/mp3"> </audio>"""


    result = html_top + '<span class="maintext">' + classifi_result + '</span><p>'+ voice_color + voice_cloth + html_bottom
    return result

@app.route('/fileUpload', methods=['GET','POST'])
def upload_file2():
    # file을 classifier를 사용하여 판별
    f = request.files['file']
    color = classifier.class_color(f)
    cloth = classifier.class_cloth(f)
    print('')
    # mp3 path 설정
    mp3_path_color = color_path + color_list[color] + '.mp3'
    mp3_path_cloth = cloth_path + cloth_list[cloth] + '.mp3'

    # 판별한 값 문자열로 변경
    color = color_list_kor[color]
    cloth = cloth_list_kor[cloth]

    # !!! json은 습관적으로 이중따옴표 사용 !!!
    return json.dumps(
        {"color":color,
        "cloth":cloth,
        "color_mp3":mp3_path_color,
        "cloth_mp3":mp3_path_cloth
        })

@app.route("/backward/", methods=['POST'])
def move_backward():
    #Moving forward code
    return render_template('A-eye.html')


# 안쓰는 코드
@app.route('/api', methods=['GET','POST'])
def api():
    # URL 매개 변수 추출하기 
    q = request.args.get('q', '')

    f = request.files['input.files[0]']
    print(f)
    color = classifier.class_color(f)
    cloth = classifier.class_cloth(f)

    return json.dumps({
        "color": 'mycolor',
        "cloth": 'hello'
    })
    

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000")