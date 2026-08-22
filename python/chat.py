import customtkinter as ctk
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import threading

llm = ChatOllama(model="mbt-ai")


# メッセージ送信
def send_message():
    user_message = input_box.get()

    if not user_message.strip():
        return

    chat_box.configure(state="normal")
    chat_box.insert("end", f"あなた: {user_message}\n\n")
    chat_box.configure(state="disabled")

    input_box.delete(0, "end")
    send_button.configure(state="disabled")

    loading.pack(fill="x", padx=20, pady=10)
    loading.start()

    thread = threading.Thread(target=ask_ollama, args=(user_message,), daemon=True)
    thread.start()


# Ollamaに問い合わせる
def ask_ollama(user_message):
    messages = [HumanMessage(content=user_message)]

    response = llm.invoke(messages)

    # GUI操作はメインスレッドに戻す
    app.after(0, show_response, response.content)


def show_response(response_text):
    loading.stop()
    loading.pack_forget()

    chat_box.configure(state="normal")
    chat_box.insert("end", f"AI: {response_text}\n\n")
    chat_box.configure(state="disabled")

    send_button.configure(state="normal")


ctk.set_appearance_mode("System")

app = ctk.CTk()
app.title("Ollama Chat")
app.geometry("700x500")

chat_box = ctk.CTkTextbox(app, width=650, height=380)
chat_box.pack(padx=20, pady=(20, 10))
chat_box.configure(state="disabled")

input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=20, pady=(0, 20))

input_box = ctk.CTkEntry(input_frame, placeholder_text="メッセージを入力してください")
input_box.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

send_button = ctk.CTkButton(input_frame, text="送信", command=send_message)
send_button.pack(side="right", padx=(5, 10), pady=10)

loading = ctk.CTkProgressBar(app, mode="indeterminate")

input_box.bind("<Return>", lambda event: send_message())

app.mainloop()
