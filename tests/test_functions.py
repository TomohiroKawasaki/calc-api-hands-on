import pytest
import azure.functions as func
import sys
import os

# src ディレクトリをモジュール検索パスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from function_app import multiply, divide


class TestMultiplyFunction:
    """掛け算 API のテスト"""
    
    def test_multiply_positive_integers(self):
        """正の整数の掛け算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': '3', 'B': '4'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '12.0'
        assert 'text/plain' in response.mimetype
    
    def test_multiply_with_decimals(self):
        """小数点を含む掛け算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': '2.5', 'B': '4'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '10.0'
    
    def test_multiply_negative_numbers(self):
        """負の数の掛け算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': '-5', 'B': '3'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '-15.0'
    
    def test_multiply_with_zero(self):
        """ゼロを含む掛け算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': '0', 'B': '100'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '0.0'
    
    def test_multiply_missing_parameter_a(self):
        """パラメータ A が欠けている場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'B': '5'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
    
    def test_multiply_missing_parameter_b(self):
        """パラメータ B が欠けている場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': '10'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
    
    def test_multiply_invalid_parameter_a(self):
        """パラメータ A が数値に変換できない場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': 'abc', 'B': '5'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
    
    def test_multiply_invalid_parameter_b(self):
        """パラメータ B が数値に変換できない場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/multiply',
            params={'A': '10', 'B': 'xyz'}
        )
        
        response = multiply(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'


class TestDivideFunction:
    """割り算 API のテスト"""
    
    def test_divide_positive_integers(self):
        """正の整数の割り算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '10', 'B': '2'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '5.0'
        assert 'text/plain' in response.mimetype
    
    def test_divide_with_decimals(self):
        """小数点を含む割り算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '7.5', 'B': '2.5'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '3.0'
    
    def test_divide_negative_numbers(self):
        """負の数の割り算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '-10', 'B': '5'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '-2.0'
    
    def test_divide_result_with_fraction(self):
        """割り切れない割り算"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '1', 'B': '2'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '0.5'
    
    def test_divide_by_zero(self):
        """ゼロ除算のエラー"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '10', 'B': '0'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '0除算です'
    
    def test_divide_missing_parameter_a(self):
        """パラメータ A が欠けている場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'B': '5'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
    
    def test_divide_missing_parameter_b(self):
        """パラメータ B が欠けている場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '10'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
    
    def test_divide_invalid_parameter_a(self):
        """パラメータ A が数値に変換できない場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': 'invalid', 'B': '5'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
    
    def test_divide_invalid_parameter_b(self):
        """パラメータ B が数値に変換できない場合"""
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/divide',
            params={'A': '10', 'B': 'error'}
        )
        
        response = divide(req)
        
        assert response.status_code == 200
        assert response.get_body().decode('utf-8') == '入力エラー: A または B が数値ではありません'
