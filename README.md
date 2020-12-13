# AI4UX (A.V.Team)
A.V.Team would love to present you with the AI that predicts your mobile application's Google Store User Rating based on your application's user interface! Human judgments are biased and flawed. When forecasting your application's user rating to your application, emotions will step into the way. Most app makers will reserve to releasing the application to the market and hope for the best. However, we are introducing a data-driven, non-bias, non-emotional AI tools that rate your app.
Here's how you can rate your app.

1. Have Python 3.8+ installed.
2. Install the libraries listed in README.md.
3. Download our repository on: https://github.com/kvkavi/AI4UXHackathonAVTeam.
4. Open up the project file. 
5. Extract the files inside ModelRF.zip.
6. Run manage.py.
7. Enter the following address into your webbrowser: http://127.0.0.1:5000/. 
    * The address may be different for you. Check the Python terminal if this is the case.
    * It will display the address in the format: "Running on http://127.0.0.1:5000/"
8. Screenshot multiple pages of your mobile application.
9. Upload the screenshots to our website by click "Choose files". 
    * The more screenshots you have, the more accurate the resut will be. 
10. Click on "Submit."
11. Our AI will present the forecasted user rating result on the site.
12. You can test out another screenshot by reuploading and clicking on "Submit" again.

Our AI utilizes data from >30,000 Google Store mobile applications, and all the applications have >100,000 downloads. These are applications includes Facebook, Slack, Livongo. We feed our model with the screenshots of the application with the final Google Store user rating. Our model will process each image, analyze the app's UI, and receive its user rating.
In the future, we can implement more data points and higher resolution images into our AI model. With more engineering resources, we can also expand the AI model algorithm to recognize the color, readability of text, and even the app's contents to be apart of our complete evaluation. With a more complex database, we can even predict other UX KPI like sessions length, session interval, session depth, average screens per visit, etc. Our AI can provide a data-driven, non-bias, and non-emotional evaluation of the app.

- pip install requirements.txt

- python3 manage.py