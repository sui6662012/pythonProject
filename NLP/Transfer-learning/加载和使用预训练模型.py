import torch

# 预训练模型来源
source = 'huggingface/pytorch-transformers'
# 选定加载模型的哪一部分，这里是模型的映射器
part = 'tokenizer'
# 加载的预训练模型的名字
model_name = 'bert-base-chinese'
tokenizer = torch.hub.load(source, part, model_name)





# 加载带/不带头的预训练模型

# 加载不带头的预训练模型
part = 'model'
model = torch.hub.load(source, part, model_name)

# 加载带有语言模型头的预训练模型
part = 'modelWithLMHead'
lm_model = torch.hub.load(source, part, model_name)

# 加载带有类模型头的预训练模型
part = 'modelForSequenceClassification'
classification_model = torch.hub.load(source, part, model_name)

# 加载带有问答模型头的预训练模型
part = 'modelForQuestionAnswering'
qa_model = torch.hub.load(source, part, model_name)

# 第四步：使用模型获得输出结果

input_text = '人生该如何起头'

# 使用tokenizer进行数值映射
indexed_tokens = tokenizer.encode(input_text)

# 打印映射后的结构
print('indexed_token:', indexed_tokens)

# 将映射结构转化为张量输送给不带头的预训练模型
tokens_tensor = torch.tensor([indexed_tokens])

# 使用不带头的预训练模型获得结果
with torch.no_grad():
    encoded_layers, _ = model(tokens_tensor)

print('不带头的模型输出结果：', encoded_layers)
print('不带头的模型输出结果的尺寸：', encoded_layers.shape)

# 使用带有语言模型头的预训练模型获得结果
with torch.no_grad():
    lm_output = lm_model(tokens_tensor)

print('带语言模型头的模型输出结果：', lm_output)
print('带语言模型头的模型输出结果的尺寸：', lm_output[0].shape)

with torch.no_grad():
    classification_output = classification_model(tokens_tensor)
print('带分类模型头的模型输出结果：', classification_output)
print('带分类模型头的模型输出结果的尺寸：', classification_output[0].shape)

# 使用带有问答模型头的模型进行输出时，需要使输入的形式为句子对
input_text1 = '我家的小狗是黑色的'
input_text2 = '我家的小狗是什么颜色的呢'

# 映射两个句子
indexed_tokens = tokenizer.encode(input_text1, input_text2)
print('句子对的indexed_tokens:', indexed_tokens)

segments_ids = [0]*11 + [1]*14

# 转化张量形式
segments_tensors = torch.tensor([segments_ids])
tokens_tensor = torch.tensor([indexed_tokens])

# 使用带有问答模型头的预训练模型获得结果
with torch.no_grad():
    start_logits, end_logits = qa_model(tokens_tensor, token_type_ids=segments_tensors)


print("带问答模型头的模型输出结果:", (start_logits, end_logits))
print("带问答模型头的模型输出结果的尺寸:", (start_logits.shape, end_logits.shape))