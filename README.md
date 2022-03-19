# sls-python-tutorial
Serverless frameworkを使ってAWS Lambdaの関数をデプロイするチュートリアル．

プラグインを使って，Pythonの依存ライブラリが使える環境を作る．



## 事前準備
以下をインストール/セットアップしておく．
- Serverless framework
- Docker
- AWSの認証情報


## 手順
### 1. サービスの作成

ServerlessでAWS Lambdaのサービスを作成する．

ここでは，`sls-python-tutorial`というサービス名にします．

```bash
sls create --template aws-python3 --path sls-python-tutorial
```

`sls-python-tutorial`ディレクトリに以下のファイルなどが生成される．
- `serverless.yml`: Serverlessの構成ファイル
- `handler.py`: 処理の関数


### 2. ブラグインのインストール
NumpyやPillowのライブラリを使えるようにするため，[serverless-python-requirements](https://www.serverless.com/plugins/serverless-python-requirements)というプラグインを使います．


```bash
# ディレクトリへ移動
cd sls-python-tutorial

# プラグインを追加
sls plugin install -n serverless-python-requirements
```

### 3. プラグインの設定を追加
`serverless.yml`に`serverless-python-requirements`用の設定を追加する．

```yml
custom:
  # serverless-python-requirementsの設定
  pythonRequirements:
    # 依存のコンパイルにdockerを使う
    dockerizePip: true
    
    # キャッシュの設定
    useDownloadCache: true
    useStaticCache: true
```

`dockerizePip`はPure-pythonではないライブラリをLinux以外のホスト(windowsやmac)からデプロイする場合は必須です．


### `requirements.txt`を作成
Pythonの依存を`requirements.txt`を書く．
```txt
numpy
Pillow
```

### ライブラリを使った処理を追加(確認用)
ここでは，ライブラリを使った処理の例として，ライブラリのバージョンを取得してレスポンスに追加する．

```python
import json

# インストールした依存をインポート
import numpy as np
import PIL.Image

import PIL
def hello(event, context):
    # ライブラリのバージョンを取得
    dependencies = {
        "numpy": np.__version__,
        "Pillow": PIL.__version__
    }
    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "dependencies": dependencies
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
```

### デプロイ
以下のコマンドでLambda関数をデプロイする．
```bash
# デプロイ
sls deploy --aws-profile <profile_name>

# 削除
sls remove --aws-profile <profile_name>
```

### 実行
以下のコマンドでデプロイされたLambda関数を実行する．
```
sls invoke -f hello
```

以下のように出力されれば成功
```json
{
    "statusCode": 200,
    "body": "{\"message\": \"Go Serverless v1.0! Your function executed successfully!\", \"input\": {}, \"dependencies\": {\"numpy\": \"1.22.3\", \"Pillow\": \"9.0.1\"}}"
}
```

## 参考
- https://www.serverless.com/framework/docs/providers/aws/cli-reference/create
- https://www.serverless.com/plugins/serverless-python-requirements