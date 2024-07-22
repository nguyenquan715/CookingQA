## Description

A cooking-related domain question-answering system that uses machine learning to provide users with a more convenient and time-saving experience in the cooking process. Specifically, this is a web application that allows users to ask questions. The system receives the question, processes it, and returns an answer to the user.

First, the question is analyzed in two steps: classifying the question using the Support Vector Machine (SVM) model and performing entity recognition using the Conditional Random Field (CRF) model. After analyzing the question, the system formats the query and executes it using the ElasticSearch (ES) search engine on a dataset of dishes. It then finds the answer and displays it to the user.

## Watch the Demo

* [![Watch the video](https://drive.google.com/file/d/1oKXV7vKWAeUG4U7TywFG7YDu0OI6RHuO/view?usp=sharing)](https://drive.google.com/file/d/1lYa4TA04m-O9zIr6oj6hD8LEd1WHB72r/view?usp=sharing)
