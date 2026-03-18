# sbpayment-papercut

PaperCut Payment Gateway with External Database Connection and

# 【前提条件】

1. パソコンに Docker がインストールされています
2. PayPay Developers / SB-Payment / GMOから統合認証情報を取得します
3. PaperCut の構成エディタにて auth.webservices.allowed-addresses にアクセス許可が設定されています
4. PaperCut の構成エディタにて auth.webservices.auth-token のが設定されています
5. 構成エディタの auth.admin-users に、少なくとも 1 名のユーザー名が設定されています（例：admin）

# 【インストール手順】

1. Docker イメージ、 docker-compose、およびNGINXの設定 ファイルをダウンロードしてください

- ppc-point-payment.tar
- nginx.tar
- docker-compose.yml
- nginx (フォルダ)

2. ファイルが圧縮されている場合は、ファイルを解凍して1つのフォルダに配置します

3. Docker ターミナルを開き、ファイルフォルダのディレクトリに移動します

4. 以下のコマンドで NGINX イメージをインポートします
   「docker load -i nginx.tar」

5. 以下のコマンドで支払システムのイメージをインポートします
   「docker load -i ppc-point-payment.tar」

6. docker-compose ファイル内の 以下の設定 の値を修正します
   -PUBLIC_URL (決済代行サーバー（SB-Payment / PayPay）がアクセス可能なサーバーパブリックアドレス)
   -PAPERCUT_SERVER (PaperCutサーバのアドレス)
   -PAPERCUT_AUTH_TOKEN (PaperCutの設定設定エディタにのauth.webservices.auth-token)
   -DATABASE (使っているデータベース, postgresqlまたはmysql)
   -DB_SERVER (データベースのサーバアドレス)
   -DB_PORT (データベースのサーバポート)
   -DB_NAME (データベースの名前)
   -DB_USERNAME (データベースのアクセスユーザ名)
   -DB_PASS (データベースのアクセスパスワード)
   -ACCESS_USERNAME (最初の設定画面のアクセスユーザ名。　PaperCutの設定設定エディタにのauth.admin-usersに記載されているユーザー名を入力してください)
   -ACCESS_PASSWORD (最初の設定画面のアクセスパスワード)
   -TZ (タイムゾーン ・ Asia/Tokyo)
   -MAIL_SERVER (メールサーバのアドレス)
   -MAIL_PORT (メールサーバのポート番号)
   -MAIL_USE_TLS (TLS が使用される場合は""True"、TLS が使用されない場合は"False")
   -MAIL_USE_SSL (SSL が使用される場合は""True"、SSL が使用されない場合は"False")
   -MAIL_USERNAME (メールサーバにアクセスできる通知の受信と送信用のメールアドレス)
   -MAIL_PASSWORD (メールのパスワード)

   ※LinuxとMac用
   [
   extra_hosts:
   - "host.docker.internal:host-gateway
     ]
     ※セクションのコメントを解除します。ホストIPアドレス（localhost）にアクセスするには、docker-composeの中で「localhost」の代わりに「host.docker.internal」を使用します。

   [
   volumes:
   ]
   セクションで、"appuser"をPC/サーバのユーザー名に置き換えます。

7. 以下のコマンドを実行して Docker コンテナをインストール・起動します
   「docker compose up -d」

8. 以下のコマンドを実行してDockerコンテナを確認します
   「docker ps」

9. 以下のコマンドを実行してDockerコンテナのログを確認します
   「docker logs -f <container-name-or-id>」

10. （任意）支払サーバーと PaperCut 接続の確認：
    http://<payment-server-address>:5050/check-connection にアクセスします

11. 設定ページにアクセスします
    http://<payment-server-address>:5050/settings-page-login
    ログインには、ACCESS_USERNAME と ACCESS_PASSWORD をご使用ください。
    これらの値は PaperCut 構成エディタにて設定・変更が可能です：
    [payment-gateway.integration.access_username] および [payment-gateway.integration.access_password]

12. 支払いプロバイダーの統合とポイント価格を設定します。決済システムの設定については、「PaperCut MF 支払いシステムの技術的な情報.pdf」にてご確認できます

13. 以下のページにアクセスし、ユーザーのポイントチャージテストを行ってください：
    http://<payment-server-ip>:5000/papercut-topup?user=<papercut-username>

14. システムのエラーログとアクセスログをダウンロードするには、ブラウザからこのURLにアクセスします。
    「http://<payment-server-address>:5050/download-application-logs-zip」

※ログは[http://<payment-server-address>:5050/settings-page-login]にログインして[アプリケーションログをダウンロード]ボタンをクリックした後にダウンロードすることもできます。

15. 一部の情報は docker ログにのみ表示されます (例: バックグラウンド プロセス)。次のコマンドを実行して、Docker ログをダウンロードします。
    「docker logs <container-name-or-id> > docker.log」
