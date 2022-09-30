# lambda-scmr-sum

## 概要

Amazon OpenSearch Service kibana から取得したデータを可視化し lambda で定期実行したものを slack へ通知する関数

## 前提

VPC 内にある Elasticsearch および kibana にはローカルマシンから直接アクセスすることができないが、SSH トンネルを使用することによって、ローカルマシンのブラウザから kibana へアクセスすることが可能となる

(参考：https://aws.amazon.com/jp/premiumsupport/knowledge-center/kibana-outside-vpc-ssh-elasticsearch/）

(1)ホームディレクトリの.ssh/config に追記

```
Host proxy
  HostName <ホスト名>
  User <iamユーザー名>
  Port <ポート>
  IdentityFile <private key>

  ProxyCommand sh -c "aws ssm start-session --target %h --profile <開発プロフィール名 or 本番プロフィール名> --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```

```
ssh proxy
```

で proxy のサーバーにログインできることを確認

(2)SOCKS プロキシを設定

(例) google chrome 拡張機能 「Proxy SwitchyOmega」

https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=ja

定義ファイルをこちらからダウンロードして、Proxy SwitchyOmega のオプション画面から import 機能を使用して定義を読み込む

https://drive.google.com/file/d/1td-myLDQMPSYYZ9i7I4frKTA2_L1gz1w/view?usp=sharing

(3)SSH トンネルを作成

以下のコマンドで SSH 接続

```
ssh proxy -ND 8157
```

コマンドはレスポンスがなく実行したままとなる

kibana にアクセス可...

## 初期設定

env/sample.yml を参考に環境変数を./env/dev.yml,　./env/prod.yml にセット

## 開発環境へのデプロイ

AWS 開発環境のプロファイルに切り替え

```
export AWS_PROFILE=<開発環境のプロファイル名>
```

serverless コマンドを使ってデプロイ

```
sls deploy
```

## 本番環境へのデプロイ

AWS 開発環境のプロファイルに切り替え

```
export AWS_PROFILE=<本番環境のプロファイル名>
```

serverless コマンドを使ってデプロイ

```
sls deploy --stage prod
```

## サーバ配布

- Python の外部モジュールを利用しているので、Serverless Framework 上で動かす際は以下コマンドで serverless-python-requirements のインストールが必須

```
npm install --save serverless-python-requirements
```
