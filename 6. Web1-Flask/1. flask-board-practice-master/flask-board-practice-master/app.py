
# 나의 프로젝트 
from flask import Flask, render_template, session, url_for, request, redirect
import pymysql

app = Flask(__name__)

# 세션의 비밀키 : 세션 데이터 암호화, 변조되지 않도록 유지하는데 사용됨
app.secret_key = 'sekey!@#'

def connectsql():
    conn = pymysql.connect(host='localhost', port=3306, user = 'root', passwd = 'Simon8463@', db = 'userlist', charset='utf8')
    return conn

# 홈페이지 
@app.route('/')
def index():
    # 세션 확인해서 로그인 정보 넘겨주기
    if 'username' in session:
        username = session['username']
        return render_template('index.html', logininfo = username)
    else:
        username = None
        return render_template('index.html', logininfo = username )

# R : 게시판 조회 
@app.route('/post')
# board테이블의 게시판 제목리스트 역순으로 출력
def post():
    # 로그인 확인
    if 'username' in session:
        username = session['username']
    else:
        
        username = None
        
    # DB 연결해서 모조리 조회해서 들고옴
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, title, wdate, view FROM board ORDER BY id DESC"
    cursor.execute(query)
    post_list = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # 렌더링 기능 
    return render_template('post.html', postlist = post_list, logininfo=username)

# R : 개별 조회 
@app.route('/post/content/<id>')
# 조회수 증가, post페이지의 게시글 클릭시 id와 content 비교 후 게시글 내용 출력
def content(id):
    if 'username' in session:
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "UPDATE board SET view = view + 1 WHERE id = %s"
        value = id
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()

        conn = connectsql()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id, title, content FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        content = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('content.html', data = content, username = username)
    else:
        return render_template ('Error.html')

# U : 수정(메소드 2개 다 받기)
@app.route('/post/edit/<id>', methods=['GET', 'POST'])
# GET -> 유지되고있는 username 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE
def edit(id):
    # post의 경우 : 
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
 
            edittitle = request.form['title']
            editcontent = request.form['content']

            conn = connectsql()
            cursor = conn.cursor()
            query = "UPDATE board SET title = %s, content = %s WHERE id = %s"
            value = (edittitle, editcontent, id)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()
    
            return render_template('editSuccess.html')
    # GET : 조회 
    else:
        # 세션 로그인 된 상태라면 DB 접속
        if 'username' in session:
            username = session['username']
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT name FROM board WHERE id = %s"
            value = id
            cursor.execute(query, value)
            # 게시글의 유저네임 모두 불러서 담기
            data = [post[0] for post in cursor.fetchall()]
            cursor.close()
            conn.close()
           
           # 게시글을 쓴 사람 중에 있으면 해당 id로 게시물 데이터 긁어오고 edit 파일 연결
            if username in data:
                conn = connectsql()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT id, title, content FROM board WHERE id = %s"
                value = id
                cursor.execute(query, value)
                postdata = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('edit.html', data=postdata, logininfo=username)
            else:
                return render_template('editError.html')
        else:
            return render_template ('Error.html')

# 삭제
@app.route('/post/delete/<id>')
# 유지되고 있는 username 세션과 id 일치시 삭제확인 팝업 연결
def delete(id):
    if 'username' in session:
        # 일단 현재 id 기준으로 DB 뒤져보기
        username = session['username']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT name FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        data = [post[0] for post in cursor.fetchall()]
        cursor.close()
        conn.close()

        # 있으면 삭제 아니면 x
        if username in data:
            return render_template('delete.html', id = id)
        else:
            return render_template('editError.html')
    else:
        return render_template ('Error.html')

# 삭제 여부 질문 페이지에서 
@app.route('/post/delete/success/<id>')
# 삭제 확인시 id와 일치하는 컬럼 삭제, 취소시 /post 페이지 연결
def deletesuccess(id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM board WHERE id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('post'))
    
# C : 생성
@app.route('/write', methods=['GET', 'POST'])
# GET -> write 페이지 연결
# POST -> username, password를 세션으로 불러온 후, form에 작성되어진 title, content를 테이블에 입력
def write():
    # 쓴 이후 post 
    if request.method == 'POST':
        # 세션의 유저네임이 있으면 그걸 받고 
        if 'username' in session:
            username = session['username']
            password = session['password']
            
            # 쓴 내용을 변수에 넣어서 전달한다 
            usertitle = request.form['title']
            usercontent = request.form['content']

            # DB에 삽입한다
            conn = connectsql()
            cursor = conn.cursor() 
            query = "INSERT INTO board (name, pass, title, content) values (%s, %s, %s, %s)"
            value = (username, password, usertitle, usercontent)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            # ??
            return redirect(url_for('post'))
        else:
            return render_template('errorpage.html')
        
    # GET : 쓰는 페이지 조회해서 쓰기
    else:
        if 'username' in session:
            username = session['username']
            return render_template ('write.html', logininfo = username)
        else:
            return render_template ('Error.html')

# 세션 해제
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# GET -> 로그인 페이지 연결
# POST -> 로그인 시 form에 입력된 id, pw를 table에 저장된 id, pw에 비교후 일치하면 로그인, id,pw 세션유지
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userid = request.form['id']
        userpw = request.form['pw']

        # 로그인 정보로 로그인 수행 
        logininfo = request.form['id']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_user WHERE user_name = %s AND user_password = %s"
        value = (userid, userpw)
        cursor.execute(query, value)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for row in data:
            data = row[0]
        
        # 데이터 있으면 정상 수행 
        # 세션에 저장하고 index 다시 불러오기 
        if data:
            session['username'] = request.form['id']
            session['password'] = request.form['pw']
            return render_template('index.html', logininfo = logininfo)
        else:
            return render_template('loginError.html')
    else:
        return render_template ('login.html')

# 회원가입 
# GET -> 회원가입 페이지 연결
# 회원가입 버튼 클릭 시, 입력된 id가 tbl_user의 컬럼에 있을 시 에러팝업, 없을 시 회원가입 성공
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        userid = request.form['id']
        userpw = request.form['pw']

        # 조회 쿼리
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_user WHERE user_name = %s"
        value = userid
        cursor.execute(query, value)
        data = (cursor.fetchall())
        #import pdb; pdb.set_trace()
        
        # 이미 있는 경우
        if data:
            conn.rollback() # 롤백 수행 
            return render_template('registError.html') 
        # 데이터 삽입(C)
        else:
            # %s value excute 
            query = "INSERT INTO tbl_user (user_name, user_password) values (%s, %s)"
            value = (userid, userpw)
            cursor.execute(query, value)
            data = cursor.fetchall()
            conn.commit()
            return render_template('registSuccess.html')
        cursor.close()
        conn.close()
    else:
        return render_template('regist.html')        

if __name__ == '__main__':
    app.run(debug=True,port=8080)