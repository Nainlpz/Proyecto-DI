def load_stylesheet():
    with open("styles.qss", encoding="utf-8") as file:
        return file.read()