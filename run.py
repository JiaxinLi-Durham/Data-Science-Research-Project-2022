from epub2txt import epub2txt
import os

filepath = 'Your path to epub file'
output = 'Your path to output file' # ending with '/'
res = epub2txt(filepath)

# 获取文件名（包含扩展名）
filename_with_extension = os.path.basename(filepath)

# 分割文件名和扩展名
filename, extension = os.path.splitext(filename_with_extension)
print(filename)

# save res to txt
with open(output+filename+'.txt', "w") as f:
    f.write(res)
def count_words(text):
    words = text.split()  # 拆分字符串成单词列表
    return len(words)  # 返回单词列表的长度


word_count = count_words(res)
print("word_count", word_count)