# News Sift Bot

Application that classifies news into positive and negative and gives the results to the user via telegrams of the bot.

It consists of four main parts:

#### 1. Parser

receives the text of articles from the site https://www.bbc.com/.

#### 2. Model

prepares data, creates features, fits Logistic Regression and gives predicts for the new articles.

#### 3. Storage

provides connections to the database.

#### 4. Telegram-bot

helps users receive news classified into positive and negative, depending on which user prefers.


## Getting started

To start using this application you need to run the following commands:

`python3 main.py migrate` - *initialize tables*,

`python3 main.py train` - *train model and save it*

`python3 main.py parse` - *parse new articles and make predict for them*

`python3 main.py run-bot` - *run telegram bot*