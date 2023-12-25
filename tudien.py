import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('input.csv')

# Lấy cột chứa văn bản cần kiểm tra lỗi chính tả
text_column = df['text']  # Thay 'text_column_name' bằng tên cột thực tế trong file CSV
# Đọc từ điển tiếng Việt
with open('vietnamese_dictionary.txt', 'r', encoding='utf-8') as file:
    vietnamese_dictionary = set(file.read().splitlines())

from nltk import ngrams
import re

def extract_words(text):
    # Loại bỏ các ký tự không phải chữ cái
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def check_spelling_errors(text, dictionary):
    # Lấy các từ từ văn bản
    words = extract_words(text)

    # Kiểm tra từng từ
    errors = []
    for word in words:
        if word not in dictionary:
            errors.append(word)

    return errors

def generate_ngrams(text, n):
    words = extract_words(text)
    ngrams_list = list(ngrams(words, n))
    return ngrams_list

# Định nghĩa hàm kiểm tra lỗi chính tả sử dụng n-gram
def check_spelling_with_ngrams(text, dictionary, n):
    ngrams_list = generate_ngrams(text, n)
    errors = []
    
    for ngram in ngrams_list:
        ngram_str = ' '.join(ngram)
        if ngram_str not in dictionary:
            errors.append(ngram_str)
    
    return errors

# Kiểm tra lỗi chính tả cho mỗi dòng trong dataframe
for index, row in df.iterrows():
    text = row['text']  # Thay 'text_column_name' bằng tên cột thực tế trong dataframe
    spelling_errors = check_spelling_with_ngrams(text, vietnamese_dictionary, 1)  # Sử dụng bigram (n=2) hoặc có thể chọn giá trị n tùy ý
    if spelling_errors:
        print(f"Lỗi chính tả Câu {index + 1}: {spelling_errors}")

from difflib import get_close_matches

def suggest_corrections(word, dictionary):
    # Tìm các từ gần giống trong từ điển
    suggestions = get_close_matches(word, dictionary, n=1, cutoff=0.8)
    if suggestions:
        return suggestions[0]
    else:
        return None

# Hàm để sửa lỗi chính tả trong văn bản
def correct_spelling_errors(text, dictionary):
    words = extract_words(text)

    corrected_text = []
    for word in words:
        if word not in dictionary:
            correction = suggest_corrections(word, dictionary)
            if correction:
                corrected_text.append(correction)
            else:
                corrected_text.append(word)
        else:
            corrected_text.append(word)

    return ' '.join(corrected_text)

# Sửa lỗi chính tả cho mỗi dòng trong dataframe
for index, row in df.iterrows():
    text = row['text']
    corrected_text = correct_spelling_errors(text, vietnamese_dictionary)
    
    # In ra văn bản gốc và văn bản đã sửa
    print(f"Original text: {text}")
    print(f"Corrected text: {corrected_text}")
    print("-----")
