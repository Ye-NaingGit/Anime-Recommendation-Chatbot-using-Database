# Anime-Recommendation-Chatbot-using-Database
This chatbot is created for Computing Research Project subject for my Higher National Diploma.The chatbot can recommend anime based on the users' inputs such as genres, rating, episode count, etc. The chatbot uses a database containing more than 10,000 anime.

![image](https://github.com/user-attachments/assets/05aa52e2-cc0f-4275-936b-cbbcc7fc6d62)

## How it is made
This chatbot is built using the RASA open source framework and Python with MySQL for the database.

## How to build
To build the chatbot locally, install RASA open source to the desired location and create a RASA project. 'Spacy' will be needed to be install if it does not come together with RASA installation. Afterwards, copy and paste the project there. Additionally, import the 'anime.sql' database so that the chatbot can get the anime to recommend. For my build, I use XAMPP to local development.

## How to Run
A trained model is included in the files so you will probably not need to train one.
Before using the trained model, you will need to run the custom actions so that the chatbot can get data from the anime database. For this, use the command "rasa run actions" in a separete terminal.
If the model does not work, a new one can be trained by using the command "rasa train" in the project directory. The trained model can be trained by using the command "rasa shell".

## Lesson Learned
By taking on this project, I have learnt a lot about how chatbots work and how to build them. Additionally, I became more proficient in coding and understanding of artificial intelligence. This is a great project as my knowledge is greatly expanded.

