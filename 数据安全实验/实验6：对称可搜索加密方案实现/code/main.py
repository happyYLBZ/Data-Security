# -*- coding: utf-8 -*-

"""
给定的代码实现了一个基本的加密和检索系统，使用陷门来处理文档。

generate_random_string函数生成给定长度的小写字母随机字符串。generate_hash函数为给定关键词生成SHA-256哈希值。generate_trapdoor函数通过获取关键词中每个字符的哈希值的第一个字符来为给定关键词生成陷门。encrypt_document函数通过将文档中每个字符添加上陷门值来加密给定文档。retrieve_documents函数从正向索引中检索包含给定关键词的文档。decrypt_document函数通过从文档中每个字符减去陷门值来解密给定文档。

主要功能是生成随机文件、为文件中每个关键字生成陷门、使用这些陷门加密文件、构建正向索引、检索包含指定关键字的文件、解密已检索到的文件，并打印原始文件和解密后的文件。

该代码使用hashlib，random和string库。
"""

import hashlib
import random
import string


# 定义一个函数，用于生成随机定长字符串
def generate_random_string(length):
    # string.ascii_lowercase包含所有小写字母
    letters = string.ascii_lowercase
    # 使用random.choice从letters中随机选择一个字母，重复length次
    # ''.join将选择的字母连接成一个字符串
    return ''.join(random.choice(letters) for i in range(length))

# 将已有的keyword生成对应的hash值
def generate_hash(keyword):
    # 使用SHA256算法对keyword进行哈希
    hash_object = hashlib.sha256(keyword.encode())
    # 返回哈希值的十六进制表示
    return hash_object.hexdigest()

# 为已有的keyword生成对应的陷门trapdoor
def generate_trapdoor(keyword):
    # 初始化陷门列表
    trapdoor = []
    # 对keyword中的每个字符进行哈希，并将哈希值的第一个字符添加到陷门列表中
    for i in range(len(keyword)):
        trapdoor.append(generate_hash(keyword[i])[0])
    # 返回陷门列表
    return trapdoor


# 加密文档
def encrypt_document(document, trapdoors):
    # 初始化加密文档列表
    encrypted_document = []
    # 遍历文档中的每个单词
    for i in range(len(document)):
        # 初始化加密单词列表
        encrypted_word = []
        # 遍历单词中的每个字符
        for j in range(len(document[i])):
            # 使用陷门对字符进行加密，然后将加密后的字符添加到加密单词列表中
            encrypted_char = chr(ord(document[i][j]) + ord(trapdoors[i][j % len(trapdoors[i])]))
            encrypted_word.append(encrypted_char)
        # 将加密单词添加到加密文档列表中
        encrypted_document.append(''.join(encrypted_word))
    # 返回加密文档
    return encrypted_document


# 通过已有的keyword查询正向索引，返回包含该keyword的文档
def retrieve_documents(keyword, index):
    # 初始化文档列表
    documents = []
    # 遍历关键词中的每个字符
    for char in keyword:
        # 如果字符在索引中，将索引中对应的文档添加到文档列表中
        if char in index:
            documents.append(set(index[char]))
    # 如果文档列表为空，返回空列表
    if len(documents) == 0:
        return []
    else:
        # 否则，返回文档列表中的交集，即包含所有关键词字符的文档
        return list(set.intersection(*documents))


# 解密文件
def decrypt_document(document, trapdoors):
    # 初始化解密文档列表
    decrypted_document = []
    # 遍历文档中的每个单词
    for i in range(len(document)):
        # 初始化解密单词列表
        decrypted_word = []
        # 遍历单词中的每个字符
        for j in range(len(document[i])):
            # 使用陷门对字符进行解密，然后将解密后的字符添加到解密单词列表中
            decrypted_char = chr(ord(document[i][j]) - ord(trapdoors[i][j % len(trapdoors[i])]))
            decrypted_word.append(decrypted_char)
        # 将解密单词添加到解密文档列表中
        decrypted_document.append(''.join(decrypted_word))
    # 返回解密文档
    return decrypted_document


# 主函数，包含了测试样例和接口调用
if __name__ == "__main__":
    # 步骤一，生成随机文档，这里为了省事都是定长的
    document = []
    for i in range(10):
        document.append(generate_random_string(5))  # 生成长度为5的随机字符串

    # 步骤二，为文档之中每个keyword生成对应的陷门trapdoor
    trapdoors = []
    for i in range(len(document)):
        trapdoors.append(generate_trapdoor(document[i]))  # 为每个关键词生成对应的陷门

    # 步骤三，使用陷门加密文档
    encrypted_document = encrypt_document(document, trapdoors)  # 使用陷门对文档进行加密

    # 步骤四，构建正向索引
    index = {}
    for i in range(len(encrypted_document)):
        for j in range(len(encrypted_document[i])):
            keyword = encrypted_document[i][j]
            if keyword not in index:
                index[keyword] = []  # 如果索引中没有这个关键词，就新建一个空列表
            index[keyword].append(i)  # 将文档的索引添加到关键词对应的列表中

    # 步骤五，检索包含指定keyword的文档
    query = encrypted_document[0][0]  # 查询的关键词
    retrieved_documents = retrieve_documents(query, index)  # 检索包含查询关键词的文档

    # 步骤六，解密已检索到的文档
    decrypted_documents = []
    for i in range(len(retrieved_documents)):
        decrypted_documents.append(decrypt_document([encrypted_document[retrieved_documents[i]]], [trapdoors[retrieved_documents[i]]])[0])  # 解密检索到的文档

    # 步骤七，打印原始文档和解密后的文档
    print("原始文档:")
    print(document)
    print("我们要查询包含 %s 的文档" % decrypt_document(query, trapdoors[0][0])[0])  # 打印查询的关键词
    print("查询到的解密后的文档:")
    print(decrypted_documents)  # 打印解密后的文档


