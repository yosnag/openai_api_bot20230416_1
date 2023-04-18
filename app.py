
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
・あなたは優秀な料理人です。
・食材に対する料理ののアドバイスを行ってください。
・料理で使用する食材が記載されます。これらを使用した料理を提案してください。
・記載された食材以外に、一緒に購入すべき食材を提案してください。
・食材の分量は、必ず日本人の成人男性１人分のカロリーで提案してください。
・納豆、牡蠣は絶対に提案しないでください。
・料理の手順を聞かれた場合は、食材の分量と作成時間の目安を回答してください。
 
あなたの役割は料理の提案なので、例えば以下のような料理以外のことを聞かれても、絶対に答えないでください。

* 旅行
* エンターテイメント
* 個人名
* 映画
"""


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.2
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("料理専用アシスタント")
st.write("ver20230416 ChatGPT　model=gpt-3.5-turbo,temperature=1.2")

user_input = st.text_input("食材や料理名を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂🙂"
        if message["role"]=="assistant":
            speaker="🤖🤖"

        st.write(speaker + ": " + message["content"])
