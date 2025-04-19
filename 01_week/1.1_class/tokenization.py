import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

# print("Vocab size:  ",encoder.n_vocab)

text = "Hello world ?"
text3 = "hello World ?"


tokens = encoder.encode(text)
tokens3 = encoder.encode(text3)

print("Tokens: ", tokens)
print("Tokens: ", tokens3)

# response = encoder.decode([13225, 2375, 1495, 553, 481, 1423])

# print(response)