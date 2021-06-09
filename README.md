# Predictions_Scores
In this project, I did one prediction model for soccer matches using statistical analysis and probability. Consider:
1. The Data was collected through one API: https://rapidapi.com/api-sports/api/api-football
2. To import the data and feed the model you can create an account in rapidapi, to get one API, and then you can use the codes:
3. partidosV3.py is the code (python3) to get the statistics of the matches using a file .txt with the ids of the matches.
4. fechasV3.py is the code (Python 3) to get the list of matches for league and rounds and results if the match is played.
5. the data retrieved of the chuck codes partidosV3.py and fechasV3.py are downloaded in one file .xls
6. In the file Laliga.xls contain the data and predictions for the season 2020-2021. Description of the sheets:
Clasificacion: In this sheet, you can see the classification table of the league, with graphs of the performance calculated
the performance was calculated considering statistics of play. The results show that the performance calculated corresponds to team position in the classification.
Cuotas: In this sheet, you can calculate the odds to the results for each match in the season.
prognostic Poisson: In this sheet, you can see the prognostic made, the model used was the Poisson curve. 
Est Partidos: In this sheet are the statistics of all matches

Results:
Using this model for predict the results showed good results, though can be improved. The next step that I'll do consist in a regression logistic model.
