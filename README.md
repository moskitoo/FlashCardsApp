Flashy Flash Card App
=====================

Flashy is a simple flash card application built using the Tkinter library in Python. It allows you to learn new words in different languages by presenting flashcards and providing options to mark words as known or unknown.

How to Use
----------

1.  Clone the repository to your local machine:

bashCopy code

`git clone https://github.com/your-username/flashy-flash-cards.git`

1.  Install the required libraries if you haven't already. You can do this using pip:

Copy code

`pip install pandas`

1.  Run the Flashy application:

Copy code

`python flashy_app.py`

1.  The Flashy application window will open.

Features
--------

-   Flash cards with words in different languages.
-   Mark words as known or unknown.
-   Words are loaded from a CSV file.
-   Data about known words is saved in a CSV file.

Usage
-----

-   The application will display a flash card with a word in your chosen language.
-   Click the "Right" button if you know the word.
-   Click the "Wrong" button if you don't know the word.
-   The application will automatically load a new word after your response.
-   Known words are saved in a CSV file for future reference.

Customization
-------------

You can customize the Flashy application by adding your own word list. Just create a CSV file with columns for different languages and their translations. Place this CSV file in the `data` folder with the name `words_to_learn_french.csv`, or specify your own file path in the `FlashyApplication` constructor.

Dependencies
------------

-   Tkinter: Python's standard GUI library.
-   Pandas: Data manipulation library for reading and writing CSV files.

Credits
-------

This Flashy Flash Card App was created by [Your Name]. You can find the source code on [GitHub](https://github.com/your-username/flashy-flash-cards).
