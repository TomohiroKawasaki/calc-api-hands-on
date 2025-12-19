import pytest
import azure.functions as func
import sys
import os

# src ディレクトリをモジュール検索パスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from function_app import multiply, divide
