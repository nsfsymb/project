import tkinter as tk

# 1. 미리 입력해둔 한방 단어 데이터 (예시 추가)
hanbang_dict = {
    "가": ["가게른", "가녘", "가돌리늄", "가잠나룻"],
    "나": ["나트륨", "나이오븀", "나프탈렌"],
    "다": ["다이아몬드", "다이옥신"],
    "라": ["라듐", "라돈"],
    "마": ["마그네슘"],
}

def check_word(event):
    search_key = entry.get().strip() # 공백 제거
    listbox.delete(0, tk.END) # 기존 리스트 초기화
    
    if not search_key:
        return
        
    # 해당 글자로 시작하는 한방 단어가 데이터에 있는지 확인
    if search_key in hanbang_dict:
        for word in hanbang_dict[search_key]:
            listbox.insert(tk.END, word)
    else:
        # 단어가 없을 때 안내 메시지
        listbox.insert(tk.END, f"'{search_key}'로 시작하는")
        listbox.insert(tk.END, "단어가 데이터에 없습니다.")

# 2. 미니 화면 구성
root = tk.Tk()
root.title("한방 헬퍼")
root.geometry("220x300") # 크기 살짝 조절
root.attributes("-topmost", True) # 항상 위에 띄우기

# 상단 안내 레이블
label = tk.Label(root, text="글자를 입력하세요 (예: 가)", font=("맑은 고딕", 10))
label.pack(pady=5)

# 입력창
entry = tk.Entry(root, font=("맑은 고딕", 14), justify="center")
entry.pack(padx=10, pady=5)
entry.bind("<KeyRelease>", check_word) # 글자가 입력될 때마다 실시간 검색

# 단어 리스트 표시창
listbox = tk.Listbox(root, font=("맑은 고딕", 12), selectmode=tk.SINGLE)
listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
