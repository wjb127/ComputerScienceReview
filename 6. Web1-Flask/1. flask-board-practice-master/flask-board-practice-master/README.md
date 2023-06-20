
#### Flask 기반 게시판 및 CRUD

---
### 1. Main
![main](https://user-images.githubusercontent.com/52586888/64872103-8a3eaf80-d681-11e9-9a21-c35d28c26aac.PNG)

---
### 1. signIn, signUp
<img src="https://user-images.githubusercontent.com/52586888/64875547-4f8c4580-d688-11e9-90d7-e5b72ebbb7b7.PNG" width="400" height="350">

템플릿 : Bootstrap

중복 아이디 체크, 회원가입 여부 검사 적용, 로그인 됬을 시 부터 계속 session 유지로 쿼리문 검사.

---
### 2. Board
![post](https://user-images.githubusercontent.com/52586888/64872132-97f43500-d681-11e9-8af6-c6f3ff91c2ef.PNG)

primary key를 id(번호)로 두고 딕셔너리 형태로 fetchall 후 출력 

---
### 3. Write, Edit
<left><img src="https://user-images.githubusercontent.com/52586888/64872139-9b87bc00-d681-11e9-8b70-29a6d26837a9.PNG" width="400" height="350"></left>
<right><img src="https://user-images.githubusercontent.com/52586888/64872143-9d517f80-d681-11e9-898d-e14490d3d76d.PNG" width="400" height="350"></right>

id값 검사 후 글 작성, 수정 시 id값과 일치하는 title, content 레코드 가져오기

---
### 4. PostView, Error
<left><img src="https://user-images.githubusercontent.com/52586888/64875551-52873600-d688-11e9-95da-faffd85a170e.PNG" width="400" height="180"></left>
<right><img src="https://user-images.githubusercontent.com/52586888/64872144-9f1b4300-d681-11e9-8b95-576332bd88f9.PNG" width="400" height="150"></right>

게시글 보기 시 카드 형식으로 출력했는데 원래 댓글 기능도 추가하려다 시간상 나중으로...

당연히 접속된 로그인정보랑 불일치하면 오류팝업

각 페이지마다 Error페이지를 따로따로 html 생성했는데 나중에 진자문법으로 통합해야겠다.

---

---
## 업데이트 해야 할 것들.
1. sqlArchemy 적용할 것.
2. 댓글 기능 추가 
3. 게시판 페이징 처리 해야함.
