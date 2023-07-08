import json
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
f = open('intents.json')
  
data = json.load(f)

print(data)  


# prepare the training data
X_train = []
y_train = []
labels = []
x = 0
for i in data:
    for j in data[i]:
        X_train.append(j)
        y_train.append(i)
        labels.append(x)
    x += 1


tokenizer = Tokenizer(num_words = 1000, oov_token = "<OOV>")
tokenizer.fit_on_texts(X_train)
vocab_size = len(tokenizer.word_index) + 1

sequences = tokenizer.texts_to_sequences(X_train)

# Pad sequences to have the same length
max_length = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')

# Convert labels to one-hot encoding
# one_hot_labels = tf.one_hot(labels, len(y_train))

# Define the TensorFlow model
# model = Sequential()
# model.add(Embedding(vocab_size, 16, input_length=max_length))
# model.add(GlobalAveragePooling1D())
# model.add(Dense(16, activation='relu'))
# model.add(Dense(len(y_train), activation='tanh'))

# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model = tf.keras.Sequential([
  keras.layers.Embedding(vocab_size, 16, input_length=max_length),
  keras.layers.Dropout(0.2),
  keras.layers.GlobalAveragePooling1D(),
  keras.layers.Dropout(0.2),
  keras.layers.Dense(1)])


model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=tf.metrics.BinaryAccuracy(threshold=0.0))


# Convert labels to numpy array
labels = tf.convert_to_tensor(labels, dtype=tf.float32)

# Train the model
model.fit(padded_sequences, labels, epochs=10)
# Train the model   
# model.fit(padded_sequences, one_hot_labels, epochs=10)

# Example text for prediction
X_test = []
y_test = []

X_test.append('increase the volume to 50%')
y_test.append('changeVolume')
X_test.append('change the volume to 50%')
y_test.append('changeVolume')
X_test.append('increase the volume')
y_test.append('changeVolume')
X_test.append('decrease the volume')
y_test.append('changeVolume')
X_test.append('decrease the volume to 50%')
y_test.append('changeVolume')
X_test.append('decrease the volume to 50%')
y_test.append('changeVolume')
X_test.append('decrease the volume to 50%')
y_test.append('changeVolume')
X_test.append('set the Volume to 50%')
y_test.append('changeVolume')
X_test.append('open music player')
y_test.append('openApp')
X_test.append('run music')
y_test.append('openApp')
X_test.append('open settings')
y_test.append('openApp')


for i in X_test:
    print(i)
    test_sequence = tokenizer.texts_to_sequences([i])
    test_padded_sequence = pad_sequences(test_sequence, maxlen=max_length, padding='post')

    # Perform prediction on the test text
    prediction = model.predict(test_padded_sequence)
    predicted_class_index = tf.argmax(prediction, axis=1).numpy()[0]
    predicted_class = y_train[predicted_class_index]

    print("Predicted class:", predicted_class)
    print("Actual class:", y_test[X_test.index(i)])
    print("")

# Tokenize and pad the test text
# test_sequence = tokenizer.texts_to_sequences(['open'])
# test_padded_sequence = pad_sequences(test_sequence, maxlen=max_length, padding='post')

# # Perform prediction on the test text
# prediction = model.predict(test_padded_sequence)
# predicted_class_index = tf.argmax(prediction, axis=1).numpy()[0]
# predicted_class = y_train[predicted_class_index]

# print("Predicted class:", predicted_class)


# # creating the vocabualry
# vocub = []
# for i in data:
#     vocub.append(i)
#     for j in data[i]:
#         vocub.append(j)

# # creating the tokenizer
# tokenizer = Tokenizer(num_words = 1000, oov_token = "<OOV>")
# tokenizer.fit_on_texts(vocub)
# word_index = tokenizer.word_index
# print(word_index)

# # creating the sequences

# seq = tokenizer.texts_to_sequences(vocub)
# print(seq)
# print(tokenizer.sequences_to_texts(seq))
# # print(tokenizer.sequences_to_texts(seq)[0])
# padded = pad_sequences(seq, padding = "post")
# print(padded)

