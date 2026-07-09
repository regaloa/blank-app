import os
import requests
import json
from dotenv import load_dotenv

# 環境変数（.env）の読み込み
load_dotenv()

# デフォルトのGemini APIキー
DEFAULT_GEMINI_KEY = "AIzaSyC2ZMIp6bXOrNiWx8xvYUlw5NN8GP2s2Bk"

def call_gemini_api(api_key, prompt):
    """Gemini APIを直接HTTPリクエストで呼び出す"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            res_data = response.json()
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Gemini API エラー: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Gemini API 接続エラー: {e}")
    return None

def call_openai_api(api_key, prompt):
    """OpenAI APIを直接HTTPリクエストで呼び出す"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "あなたは優秀なプログラミング教師です。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            res_data = response.json()
            return res_data['choices'][0]['message']['content']
        else:
            print(f"OpenAI API エラー: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"OpenAI API 接続エラー: {e}")
    return None

def generate_mock_advice(category):
    """API呼び出しが失敗したときの親切なデフォルト回答"""
    return (
        f"【お知らせ: API接続エラー中のため定型アドバイス】\n"
        f"「{category}」ですね！難しく感じるかもしれませんが、まずは短いコードを動かすことから始めましょう。"
        f"次回は基礎文法を確認し、実際に手を動かす簡単な練習問題に進みましょう！"
    )

def generate_advice(category, provider="Gemini"):
    """
    指定された分野に対してアドバイスを生成する (Gemini or OpenAI)
    """
    prompt = f"""
あなたはプログラミング学習を支援する先生です。

学習者の苦手分野は「{category}」です。

以下の条件でアドバイスしてください。

・100文字程度
・初心者向け
・優しい文章
・次に学ぶ内容も提案する
"""

    result = None

    if provider == "Gemini":
        api_key = os.getenv("GOOGLE_API_KEY") or DEFAULT_GEMINI_KEY
        if api_key:
            result = call_gemini_api(api_key, prompt)

    elif provider == "OpenAI":
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            result = call_openai_api(api_key, prompt)

    # 【重要】結果があればそれを返し、失敗・キー不足ならモックを返す処理を追加
    if result:
        return result
    else:
        return generate_mock_advice(category)
