# ローカルLLM

## 概要
このプロジェクトは、local LLMを使用するためのサンプルコードです。以下の手順でセットアップと実行が可能です。
## セットアップ手順
1. **Ollamaをインストール**
   - Ollamaの公式サイトからインストール手順に従ってください。
2. **Ollamaのにてlocal LLMをダウンロード**
   - 以下のコマンドを実行して、local LLMをダウンロードします。
     ```bash
     ollama pull ローカルLLMの名前
     ```
3. **OllamaのAPIを起動**
    - 以下のコマンドを実行して、OllamaのAPIを起
    動します。
      ```bash
      ollama serve
      ```
4. **Pythonの依存関係をインストール**
   - 以下のコマンドを実行して、Pythonの依存関係をインストールします。
     ```bash
     pip install -r requirements.txt
     ```
5. **FastAPIを起動**
   - 以下のコマンドを実行して、FastAPIを起動します。
     ```bash
     uvicorn main:app --host 

