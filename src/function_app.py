import azure.functions as func
import logging
from typing import Optional, Tuple

# Function App の初期化
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def validate_and_parse_params(req: func.HttpRequest) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    クエリパラメータ A, B を検証し、浮動小数点数に変換する
    
    Returns:
        (a_value, b_value, error_message)
        - 成功時: (float, float, None)
        - 失敗時: (None, None, エラーメッセージ)
    """
    a_str = req.params.get('A')
    b_str = req.params.get('B')
    
    # 必須パラメータのチェック
    if not a_str or not b_str:
        return None, None, "入力エラー: A または B が数値ではありません"
    
    # 数値変換の試行
    try:
        a_value = float(a_str)
        b_value = float(b_str)
        return a_value, b_value, None
    except ValueError:
        return None, None, "入力エラー: A または B が数値ではありません"


@app.route(route="multiply", methods=["GET"])
def multiply(req: func.HttpRequest) -> func.HttpResponse:
    """
    掛け算 API: GET /api/multiply?A=<num>&B=<num>
    
    Returns:
        - 正常時: A × B の計算結果 (text/plain)
        - エラー時: エラーメッセージ (text/plain)
    """
    logging.info('multiply 関数が呼び出されました')
    
    # パラメータの検証と解析
    a_value, b_value, error_msg = validate_and_parse_params(req)
    
    if error_msg:
        logging.warning(f'multiply: {error_msg} (A={req.params.get("A")}, B={req.params.get("B")})')
        return func.HttpResponse(
            error_msg,
            status_code=200,
            mimetype="text/plain",
            charset="utf-8"
        )
    
    # 計算実行
    result = a_value * b_value
    logging.info(f'multiply: {a_value} × {b_value} = {result}')
    
    return func.HttpResponse(
        str(result),
        status_code=200,
        mimetype="text/plain",
        charset="utf-8"
    )


@app.route(route="divide", methods=["GET"])
def divide(req: func.HttpRequest) -> func.HttpResponse:
    """
    割り算 API: GET /api/divide?A=<num>&B=<num>
    
    Returns:
        - 正常時: A ÷ B の計算結果 (text/plain)
        - エラー時: エラーメッセージ (text/plain)
    """
    logging.info('divide 関数が呼び出されました')
    
    # パラメータの検証と解析
    a_value, b_value, error_msg = validate_and_parse_params(req)
    
    if error_msg:
        logging.warning(f'divide: {error_msg} (A={req.params.get("A")}, B={req.params.get("B")})')
        return func.HttpResponse(
            error_msg,
            status_code=200,
            mimetype="text/plain",
            charset="utf-8"
        )
    
    # ゼロ除算のチェック
    if b_value == 0:
        logging.warning(f'divide: 0除算エラー (A={a_value}, B={b_value})')
        return func.HttpResponse(
            "0除算です",
            status_code=200,
            mimetype="text/plain",
            charset="utf-8"
        )
    
    # 計算実行
    result = a_value / b_value
    logging.info(f'divide: {a_value} ÷ {b_value} = {result}')
    
    return func.HttpResponse(
        str(result),
        status_code=200,
        mimetype="text/plain",
        charset="utf-8"
    )
