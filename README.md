# Calc API Hands-on

Azure Functions (Python 3.11) で実装した掛け算・割り算 API です。

## 📋 API 仕様

### 掛け算 API
- **エンドポイント**: `GET /api/multiply`
- **パラメータ**: `A` (数値), `B` (数値)
- **例**: `/api/multiply?A=3&B=4` → `12.0`

### 割り算 API
- **エンドポイント**: `GET /api/divide`
- **パラメータ**: `A` (数値), `B` (数値)
- **例**: `/api/divide?A=10&B=2` → `5.0`

## 🚀 ローカル開発

### 前提条件
- Python 3.11
- Azure Functions Core Tools v4
- Azure CLI

### セットアップ

```bash
# 1. 依存パッケージのインストール
cd src
pip install -r requirements.txt

# 2. ローカル設定ファイルの作成
cp local.settings.json.example local.settings.json

# 3. Functions の起動
func start
```

### テストの実行

```bash
# テスト用パッケージのインストール
cd tests
pip install -r requirements.txt

# テストの実行
pytest -v
```

## 📦 デプロイ

### GitHub Actions によるデプロイ

1. **Azure リソースの作成** (東日本リージョン)
   - Resource Group: `rg-calcapi-jpe-prod`
   - Function App: `func-calcapi-jpe-prod` (Linux, Python 3.11, Consumption)
   - Storage Account: `stcalcjpe<random>`
   - Application Insights: `appi-calcapi-jpe-prod`

2. **OIDC 認証の設定**
   - Azure AD にアプリ登録を作成
   - Federated Credentials を設定
   - GitHub Secrets に以下を追加:
     - `AZURE_CLIENT_ID`
     - `AZURE_TENANT_ID`
     - `AZURE_SUBSCRIPTION_ID`

3. **App Settings の設定**
   ```bash
   az functionapp config appsettings set \
     --name func-calcapi-jpe-prod \
     --resource-group rg-calcapi-jpe-prod \
     --settings \
       WEBSITE_RUN_FROM_PACKAGE=1 \
       FUNCTIONS_EXTENSION_VERSION=~4 \
       FUNCTIONS_WORKER_RUNTIME=python
   ```

4. **デプロイの実行**
   - `main` ブランチへの push で自動デプロイ
   - または GitHub Actions の「Run workflow」から手動実行

## 📁 プロジェクト構成

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions ワークフロー
├── docs/
│   ├── requirements.md         # 機能要件
│   └── nonrequirements.md      # 非機能要件
├── src/
│   ├── function_app.py         # メインアプリケーション
│   ├── host.json               # Functions ホスト設定
│   ├── requirements.txt        # Python 依存パッケージ
│   ├── local.settings.json.example  # ローカル設定テンプレート
│   └── .funcignore             # デプロイ除外ファイル
└── tests/
    ├── conftest.py             # pytest 設定
    ├── test_functions.py       # 単体テスト
    └── requirements.txt        # テスト用依存パッケージ
```

## 🧪 テストケース

- ✅ 正常系: 整数・小数・負の数の計算
- ✅ 異常系: パラメータ欠如、不正な値、0除算

## 📊 監視

- Application Insights でログとテレメトリを収集
- Azure Portal からメトリクスとログを確認可能
