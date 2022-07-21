# Installation04
Cryptocurrency price movement prediction project using machine learning.
this project was not easy, i worked on it for close to 8 months as my graduation project, from data collection to processing to model training and selection,
to finally the website design and implementation.
This repo contains all the code and data that represent this project and the work i put into it.
1-  Data,
  put into CSV files, the different types of data that after researching and collecting were found to be best for NN model training.
  the data is clean, contains no jumps or duplicates, all the gaps were filled using constant or linear interpolation , based on what worked best.

2- Code for training NN models on that data,
  the code added contains the final iteration of the feature creation and data preprocessing process.
  its made modular in a way that makes it easy to try multiple types of data and settings for the training.
 
3- Website project files, 
  the website is made using flask, the full project files including the latest models, model files and scalers are included.
  except the database, which needs to be in "WebsiteProjectFiles/App/CryptoDB.db", it must contain the past 3 months of data for the models to run 
  correctly, if there is missing data the models will run but the results will not be accurate.

4- Data collection programs,
  for the website to update all of the models correctly it needs to get real-time data for the models, and so it uses alot of websites to get this data.
