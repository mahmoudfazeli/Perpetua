'''
Author: Arezoo Abdollahi
I write a simple flask web application which shows the logo fo the company and then it will shows top 5 hotel name
'''

from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)



@app.route('/')
def form():
    return """
        <html>
            <body>
                <div align="center">
                    <div> 
                        <img width=100px height=100px src="logo.jpg" alt="Perpetua_Logo">
                    </div>
                    
                    
                        <h1>Revotel - A Hotel Review Service </h1>
                        <h5>Below is our recommendation for your travel</h5>

                        <form action="/reviewRanker" method="post" enctype="multipart/form-data">
                            

                        </form>
                </div>
            </body>
        </html>
    """

@app.route('/reviewRanker', methods=["GET","POST"])
def reviewRanker():
	data = pd.read_csv('hotel_reviews.csv')

	data = data.dropna(axis=0, subset=['reviews_text'])
	data = data.dropna(axis=0, subset=['reviews_title'])

	# extracting the year of the reviews
	data['reviews_date'] = pd.to_datetime(data['reviews_date'])
	year_review = pd.to_datetime(data['reviews_date']).dt.year
	year_review.unique()


	frame = { 'HotelName': data['name'], 'ReviewYear': year_review, 'Rate': data['reviews_rating']} 
	data_NRY = pd.DataFrame(frame)  #Data_NameReviewYear
	data_NRY.head(5)


	data_NRY.loc[data_NRY['HotelName'] =='Suncoast Hotel and Casino'].count()


	### here, I wanted to display the top 5 hotels which has the highest number of votes and mean 
	grouped_multiple_y = data_NRY.groupby(['HotelName', 'ReviewYear']).agg({'Rate': ['count','mean', 'min', 'max']})
	grouped_multiple_y.columns = ['count','rate_mean', 'rate_min', 'rate_max']
	grouped_multiple_y = grouped_multiple_y.reset_index().sort_values(by='count', ascending=False)
	#print(str(grouped_multiple_y.head(5)))
	 

	return (str(grouped_multiple_y.head(5).HotelName))
	


if __name__  == '__main__':
	app.run(debug=True)