import customtkinter as ctk
import requests

# הגדרת גופן עברי
font_hebrew = ("David", 18)

# פונקציה לחיפוש ספרים
def search_books():
    query = search_entry.get()
    if not query:
        result_label.configure(text="❌ אנא הכנס שם ספר")
        return
    
    try:
        response = requests.get(f"http://127.0.0.1:8000/search?query={query}")
        if response.status_code == 200:
            books = response.json()
            display_results(books)
        else:
            result_label.configure(text="⚠ שגיאה בחיפוש הספרים")
    except Exception as e:
        result_label.configure(text=f"⚠ שגיאה: {e}")

# פונקציה להצגת התוצאות עם יישור לימין
def display_results(books):
    results_textbox.configure(state="normal")  # לאפשר עריכה זמנית
    results_textbox.delete("0.0", "end")  # לנקות תוכן קודם
    
    if books:
        for book in books:
            # הוספת תו Unicode (RLE - Right-to-Left Embedding) ליישור לימין
            results_textbox.insert("end", f"\u202b📖 {book['title']} - {book['author']}\n")
    else:
        results_textbox.insert("end", "\u202b❌ לא נמצאו ספרים")
    
    results_textbox.configure(state="disabled")  # לנעול שוב את התיבה

# יצירת חלון ראשי
root = ctk.CTk()
root.title("📚 אפליקציית חיפוש ספרים")
root.state("zoomed")

# הוספת השורה לווידוא שהחלון תמיד נפתח במצב מוגדל
root.after(100, lambda: root.state("zoomed"))

# מסגרת ראשית
frame = ctk.CTkFrame(root)
frame.pack(expand=True, fill="both")

# תיבת חיפוש ממורכזת עם יישור טקסט לימין
search_entry = ctk.CTkEntry(frame, 
                            placeholder_text="🔎 חפש ספר...", 
                            width=400, 
                            height=40, 
                            font=font_hebrew,
                            justify="right")  
search_entry.pack(pady=10, anchor="center")  

# כפתור חיפוש
search_button = ctk.CTkButton(frame, text="🔍 חפש", font=font_hebrew, command=search_books)
search_button.pack(pady=10)

# מסגרת לתיבת התוצאות
results_frame = ctk.CTkFrame(frame)
results_frame.pack(pady=10, anchor="center")  

# תיבת תוצאות ממורכזת עם טקסט מיושר לימין
results_textbox = ctk.CTkTextbox(results_frame, width=500, height=300, font=font_hebrew)
results_textbox.pack()
results_textbox.configure(state="disabled")  # מניעת עריכה ידנית

# תווית להודעות שגיאה
result_label = ctk.CTkLabel(frame, text="", font=font_hebrew)
result_label.pack(pady=5)

root.mainloop()
