# -*- coding: utf-8 -*-
"""Breast Cancer Prediction PyTorch.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ndiXx7Ai4JJUTIZdZW6Lpg4M4zTpOQXG

**Import Dependencies**
"""

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

"""**Device Configuration**"""

# check for CUDA availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

"""**Data Collection and Preprocessing**"""

#load the breast cancer
data = load_breast_cancer()
X = data.data
Y = data.target

print(X)

print(Y)

# split the dataset into training and test set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print(X.shape)
print(X_train.shape)
print(X_test.shape)

# standardize the data using Standard Scaler
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

type(X_train)

# convert data to PyTorch tensors and move it to GPU
X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
Y_train = torch.tensor(Y_train, dtype=torch.float32).to(device)
X_test = torch.tensor(X_test, dtype=torch.float32).to(device)
Y_test = torch.tensor(Y_test, dtype=torch.float32).to(device)

"""**Neural Netowrk Architecture**"""

# define the neural network architecture

class NeuralNet(nn.Module):

  def __init__(self, input_size, hidden_size, output_size):
    super(NeuralNet, self).__init__()
    self.fc1 = nn.Linear(input_size, hidden_size)
    self.relu = nn.ReLU()
    self.fc2 = nn.Linear(hidden_size, output_size)
    self.sigmoid = nn.Sigmoid()

  def forward(self, x):
    out = self.fc1(x)
    out = self.relu(out)
    out = self.fc2(out)
    out = self.sigmoid(out)
    return out

# define hyperparameters
input_size = X_train.shape[1]
hidden_size = 64
output_size = 1
learning_rate = 0.001
num_epochs = 100

# initialize the neural network and move it to the GPU
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# define loss and the optimizer
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

"""**Training the Neural Network**"""

# training the model
for epoch in range(num_epochs):
  model.train()
  optimizer.zero_grad()
  outputs = model(X_train)
  loss = criterion(outputs, Y_train.view(-1,1))
  loss.backward()
  optimizer.step()

  #calculate the accuracy
  with torch.no_grad():
    predicted = outputs.round()
    correct = (predicted == Y_train.view(-1,1)).float().sum()
    accuracy = correct/Y_train.size(0)

  if (epoch+1) % 10 == 0:
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss : {loss.item():.4f}, Accuracy: {accuracy.item() * 100:.2f}%")

"""**Model Evaluation**"""

# evalution on training set
model.eval()
with torch.no_grad():
  outputs = model(X_train)
  predicted = outputs.round()
  correct = (predicted == Y_train.view(-1,1)).float().sum()
  accuracy = correct/Y_train.size(0)
  print(f"Accuracy on Training Data: {accuracy.item() * 100:.2f}%")

# evalution on training set
model.eval()
with torch.no_grad():
  outputs = model(X_test)
  predicted = outputs.round()
  correct = (predicted == Y_test.view(-1,1)).float().sum()
  accuracy = correct/Y_test.size(0)
  print(f"Accuracy on Testing Data: {accuracy.item() * 100:.2f}%")
