#use this thing if you want the bot to open every file in a location
import os
text_location = []


def find_text_files():
    # text_location = []
    for root, _, files in os.walk(r'C:/Users/USER/Desktop/autosearch_test'):
        for file in files:
            if file.endswith(r".txt"):
                file_path = os.path.join(root, file).replace("\\", '/')
                # file_path.replace(r"\\", r"/")
                text_location.append(file_path)
                # text_location[r"\\"] = "/"

    return text_location

find_text_files()
print(text_location)
