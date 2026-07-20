import tiktoken

# enc = tiktoken.encoding_for_model("gpt-4")

# print(enc.encode("Hello, how are you?"))

# decode = enc.decode([9906, 11, 1268, 527, 499, 30])
# print(decode)

enc = tiktoken.get_encoding("cl100k_base")
print(enc.encode("Hello, how are you?"))