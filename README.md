# Automatic-Snake-with-ML-techniques
## determining the movement of the Snake game with Machine Learning classification models

Authors Hugo Centeno & Javier Calvo

Last commit 11th April 2024

### Notes:
- This project combines Python and Weka (Waikato Environment for Knowledge Analysis).
- Python is used to define the logic and display of the game. As well to wwrite and store the dataset latter used for classification.
- Weka is used to generate classification models based on the stored data.

### Brief description of the project:
The aim of this project was to automatize the movement of the snake game to optimize the score.

The choice of where to move would be determined by a classification algorithm, where each movement was encoded as: 0, 1, 2, 3 (U, D, R, L).


### Phases of the project:
#### 1. Building the test set (Python) :
Different algorithms were coded to determine the movement of the snake. Basic situations such as colliding with the walls or colliding with itself were avoided.

For every frame, different information such as the position of the head, the position of the apple or the current direction where written in the a *.arf* file.

#### 2. Obtainig the classification model (Weka):
With part of the *.arf* as train set and part as test set we predicted and checked with different models the accuracy of the next movement the snake was supposed to do to avoid colliding.

### Considerations to run the project
-To get new models or analyze the accuracy of the ones provided in the repository Weka should be used. More info.:https://ml.cms.waikato.ac.nz/weka

-Paths writting the *.arf* file should be modified.

-Commented lines in *Snake_savearff.py* should be uncommented if one wants the movement of the Snake to be determined by classification algorithms and not by the basic movement algorithms initially implemented.


### Program preview

