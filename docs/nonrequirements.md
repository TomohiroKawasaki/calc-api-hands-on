# 非機能要件（Non-Functional Requirements）

## 1. クラウド/リージョン/プラン
- プラットフォーム: Microsoft Azure
- リージョン: 東日本（Japan East）
- サービス: Azure Functions v4（Python）
- ランタイム/OS: Python 3.11 / Linux
- スケーリング: Consumption プラン（ゼロスケール/コールドスタートあり）

## 2. 可用性・性能
- SLO/性能目標: なし（明示の数値目標は設定しない）
- タイムアウト: 既定の範囲（HTTP は長時間実行を想定しない）
- コールドスタート: 許容

## 3. セキュリティ/認証
- 認証レベル: ANONYMOUS（公開）
- AAD/関数キー: 不要
- 秘密情報: コードに直書きしない（App Settings/Key Vault 等で管理）

## 4. CORS
- 方針: ブラウザのアドレスバー直接アクセスを主用途とし、現時点では特別な CORS 設定は不要。
- 付記: フロントエンド（XHR/Fetch）などクロスオリジンからの呼び出しが発生する場合、許可オリジンを明示設定する。

## 5. ログ/監視
- 監視: Application Insights 有効化
- ログ: Python `logging` を使用し、関数ごとにリクエスト/入力検証/結果/エラーを記録
- サンプリング/保持期間: 既定値（必要に応じて後日調整）

## 6. デプロイ/運用
- CI/CD: GitHub Actions を利用
  - 推奨: OIDC で `azure/login` 実行 → Zip Deploy（Run From Package）
  - 推奨アプリ設定: `WEBSITE_RUN_FROM_PACKAGE`（パッケージからの実行）
- 必須リソース/設定:
  - `AzureWebJobsStorage`（ストレージアカウント GPv2）
  - `FUNCTIONS_EXTENSION_VERSION=v4`
  - `APPLICATIONINSIGHTS_CONNECTION_STRING`（または旧 `APPINSIGHTS_INSTRUMENTATIONKEY`）

## 7. 命名規約（例）
- 環境接尾辞: `<env>` を `dev/stg/prd` 等で置換
- 例:
  - リソースグループ: `rg-calcapi-jpe-<env>`
  - Function App: `func-calcapi-jpe-<env>`
  - ストレージ: `stcalcjpe<unique>`
  - App Insights: `appi-calcapi-jpe-<env>`

## 8. 運用ポリシー
- 変更管理: Pull Request ベース／CI でビルド・デプロイを自動化
- 障害対応: App Insights の失敗率/ログから切り分け。必要に応じてワークアイテム化
- コスト: Consumption プランの従量課金を前提（監視コストも含め最適化は必要に応じ実施）

## 9. その他の考慮事項
- 文字コード: UTF-8、応答は日本語プレーンテキスト
- 国際化/i18n: 現時点では対象外
- 将来性メモ: 将来的にプラン見直し（例: Flex Consumption）を検討する可能性あり
