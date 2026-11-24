import arabic_reshaper
from bidi.algorithm import get_display


def prepare_persian(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


# pip install arabic-reshaper python-bidi

# label = tk.Label(
#     root,
#     text=prepare_persian("لیست کارهای من"),
#     font=("Tahoma", 12),
#     anchor="e",
#     justify="right"
# )
# label.pack(fill="x")


# entry = tk.Entry(
#     root,
#     font=("Tahoma", 12),
#     justify="right"
# )
# entry.pack()
