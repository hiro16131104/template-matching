## 目次
- [目次](#目次)
- [利用者向け](#利用者向け)
  - [概要](#概要)
  - [前提](#前提)
  - [検証環境](#検証環境)
  - [事前準備](#事前準備)
  - [仮想環境を構築し、起動する](#仮想環境を構築し起動する)
  - [Pythonスクリプトを実行する](#pythonスクリプトを実行する)
  - [仮想環境を終了する](#仮想環境を終了する)
- [開発者向け（自分用メモ）](#開発者向け自分用メモ)
  - [プロジェクトを作成し、git管理にする](#プロジェクトを作成しgit管理にする)
  - [仮想環境を作成する](#仮想環境を作成する)
  - [仮想環境を起動し、パッケージ管理ツールをアップデートする](#仮想環境を起動しパッケージ管理ツールをアップデートする)
  - [フォーマッター、リンター等をインストールする](#フォーマッターリンター等をインストールする)
  - [Pythonファイル、その他の設定を作成する](#pythonファイルその他の設定を作成する)
  - [blackと競合しないようにflake8の設定を変更する](#blackと競合しないようにflake8の設定を変更する)
  - [isortの設定を変更する](#isortの設定を変更する)
  - [その他の依存パッケージを追加、削除する](#その他の依存パッケージを追加削除する)
  - [フォーマッター、リンター等を使用する](#フォーマッターリンター等を使用する)
  - [Pythonファイルを実行する](#pythonファイルを実行する)
  - [仮想環境を終了する](#仮想環境を終了する-1)

<br>

## 利用者向け

### 概要
- ある画像の中に、もう一方の画像に似た箇所が含まれているかを検索するためのツール
- 被検索対象画像（image）の各部位と検索対象画像（template）との類似度を計算し、閾値を超えているものを抽出する
- ユーザーが事前に用意した設定を基に、抽出結果（範囲）に名前を付ける
- 抽出結果を画像にマッピング（画像に枠線を記載する）して出力する
- 抽出結果をCSVファイルとして出力する

### 前提
- Pythonがインストール済みである
- Poetry（Pythonのパッケージ管理ツール）がインストール済みである

### 検証環境
- macOS version14.5

### 事前準備
- 被検索対象の画像ファイル（image）と検索対象の画像ファイル（template）を"./assets/images/input"に格納する
- "./config/named-ranges.json"を編集し、抽出結果（範囲）に名前をつけるための設定を行う
- 類似度の閾値を変更したい場合は".env"ファイルの"THRESHOLD"を編集する

### 仮想環境を構築し、起動する
```
poetry install
poetry shell
```

### Pythonスクリプトを実行する
```
python ./src/app.py
```

### 仮想環境を終了する
```
exit
```

<br>

## 開発者向け（自分用メモ）
### プロジェクトを作成し、git管理にする
```
mkdir template_matching
cd ./template_matching
git init
```

### 仮想環境を作成する
```
poetry init
poetry config virtualenvs.in-project true
poetry env use 3.11
poetry install
```

### 仮想環境を起動し、パッケージ管理ツールをアップデートする
```
poetry shell
poetry self update
```

### フォーマッター、リンター等をインストールする
```
poetry add black flake8 isort
```

### Pythonファイル、その他の設定を作成する
```
mkdir src
touch ./src/app.py
touch .flake8 .env .gitignore
```

### blackと競合しないようにflake8の設定を変更する
``` 
# .flake8に記載する
[flake8]
max-line-length = 88
extend-ignore = E203
```

### isortの設定を変更する
```
# pyproject.tomlに追記する
[tool.isort]
profile = "black"
```

### その他の依存パッケージを追加、削除する
```
poetry add <package-name>
poetry remove <package-name>
```

### フォーマッター、リンター等を使用する
```
black ./src/
isort ./src/
flake8 ./src/
```

### Pythonファイルを実行する
```
python ./src/app.py
```

### 仮想環境を終了する
```
exit
```
