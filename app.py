from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st
import os

load_dotenv()

# システムプロンプトの定義
SYSTEM_PROMPTS = {
    "メンタルケア専門家": """
        あなたは経験豊富なメンタルケアの専門家です。
        以下の点に注意して回答してください：
        - 共感的で温かみのある表現を使用する
        - 心理学的な知見に基づいたアドバイスを提供する
        - 具体的で実践可能な解決策を提案する
        - 必要に応じて専門機関への相談を勧める
        - 日本語で丁寧に回答する
        """,
    "睡眠専門家": """
        あなたは睡眠医学の専門家です。
        以下の点に注意して回答してください：
        - 科学的根拠に基づいた睡眠に関するアドバイスを提供する
        - 睡眠の質を改善する具体的な方法を提案する
        - 生活習慣の改善点を明確に示す
        - 睡眠障害が疑われる場合は医療機関への相談を勧める
        - 日本語で分かりやすく回答する
        """
}

# LLMの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# UI構築
st.title("🧠💤 メンタルケアと睡眠に関する質問ができるWebアプリ")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["メンタルケア専門家", "睡眠専門家"]
)

st.divider()

# 入力フォーム
input_message = st.text_input(f"{selected_item}に関する質問を入力してください。")

# 実行ボタンの処理
if st.button("実行"):
    st.divider()
    
    if not input_message:
        st.error("質問を入力してから「実行」ボタンを押してください。")
    else:
        # メッセージ作成と送信
        messages = [
            SystemMessage(content=SYSTEM_PROMPTS[selected_item]),
            HumanMessage(content=input_message)
        ]
        
        with st.spinner(f"{selected_item}が回答を作成中..."):
            response = llm.invoke(messages)
            
        # 回答表示
        emoji = "🧠" if selected_item == "メンタルケア専門家" else "💤"
        st.success(f"{emoji} {selected_item}からの回答:")
        st.write(response.content)