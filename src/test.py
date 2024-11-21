from transformers import BartTokenizer

# 加载模型
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# 打印模型的缓存路径
print(tokenizer.pretrained_vocab_files_map)  # 这将列出模型相关文件的路径
