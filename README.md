# AIClassProject
- Ryan Romero         rromero26@csu.fullerton.edu
- Peter Bergeon       peterbergeon@csu.fullerton.edu
- Brian Edwards       brian_edwards@csu.fullerton.edu

# Project Description
Despite every member of the group attending fullerton for over 3+ years, many of us still struggle navigating the CSUF portal/domain, as well as the updated Student Center. We want to offer a solution to that small problem.
We will be creating a conversational AI bot that users can ask questions specifically about the CSUF portal to help navigate through the website. Instead of students struggling through the website seeking out what they need, users can ask the bot 1 or 2 questions. The bot responds with the information needed or straightforward instructions to get to where the user needs.
To respond to the users questions, the bot will take the user’s question string, analyze for certain keywords. With these keywords, it determines what the user may be asking and spit out text responding to the user’s inquiry. If the bot does not have sufficient keywords to pinpoint a proper response, it will ask the user questions until it has enough keyword information to determine what to respond.

# How to Run
Before running the python files, make sure you have the following libraries installed on your workstation:
- numpy
- nltk  (natural language toolkit)
- tensorflow


1. Download the files and save them to any desired location on your computer
2. Open terminal and navigate to the AI project files
3. Run "training.py" first (will take a few seconds for training model to complete)
4. Run "main.py" second
