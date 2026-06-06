import tkinter as tk

# 1. 미리 입력해둔 한방 단어 데이터 (예시)
hanbang_dict = {
    "가": ["가게른", "가녘", "가돌리늄", "가잠나룻"],
    "나": ["나트륨", "나이오븀", "나프탈렌"],
    "다": ["다이아몬드", "다이옥신"],
    # ... 계속 추가
}

def check_word(event):
    search_key = entry.get() # 사용자가 입력한 글자
    listbox.delete(0, tk.END) # 기존 리스트 초기화
    
    # 해당 글자로 시작하는 한방 단어가 있다면 리스트에 표시
    if search_key in hanbang_dict:
        for word in hanbang_dict[search_key]:
            listbox.insert(tk.END, word)

# 2. 미니 화면 구성
root = tk.Tk()
root.title("한방 헬퍼")
root.geometry("200x250") # 작게 만들기
root.attributes("-topmost", True) # ★항상 위에 띄우기

# 입력창
entry = tk.Entry(root, font=("맑은 고딕", 14))
entry.pack(padx=10, pady=5)
entry.bind("<KeyRelease>", check_word) # 글자가 입력될 때마다 함수 실행

# 단어 리스트 표시창
listbox = tk.Listbox(root, font=("맑은 고딕", 12))
listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
