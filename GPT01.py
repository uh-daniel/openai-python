from flask import Flask, render_template, request

app = Flask(__name__)

# 대화 기록을 저장할 리스트
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 웹 화면에서 전송된 메시지 받기
        message = request.form['message']

        # 대화 기록에 메시지 추가
        chat_history.append(message)

        # 여기서는 받은 메시지를 그대로 출력
        # 원하는 동작에 따라 원하는 응답을 구현할 수 있습니다.
        response = message

        # 대화 기록과 응답을 함께 전달
        return render_template('index.html', chat_history=chat_history, response=response)

    # GET 요청이면 초기 화면을 보여줌
    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run()