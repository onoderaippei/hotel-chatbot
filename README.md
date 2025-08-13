🖥 サーバー起動方法
1. 環境変数設定（Tomcatパス）
bash
コピーする
編集する
export CATALINA_HOME="$(brew --prefix tomcat)/libexec"
2. バックエンド（FastAPI）
bash
コピーする
編集する
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
起動後: http://127.0.0.1:8000/docs

3. フロントエンド（Tomcat + JSP）
bash
コピーする
編集する
cd frontend
mvn package
cp target/frontend.war "$CATALINA_HOME/webapps/"
"$CATALINA_HOME/bin/catalina.sh" start
起動後: http://localhost:8080/frontend/chat.jsp

4. サーバー停止（Tomcat）
bash
コピーする
編集する
"$CATALINA_HOME/bin/catalina.sh" stop
