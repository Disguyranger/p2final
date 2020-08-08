import os, sqlalchemy, pymysql
import pandas as pd
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine


# Heroku check
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True

# Import your config file(s) and variable(s)
if is_heroku == False:
    from config import host, port, username, password, database 
else:
    host = os.environ.get('host')
    port = os.environ.get('port')
    username = os.environ.get('username')
    password = os.environ.get('password')
    database = os.environ.get('database')

pymysql.install_as_MySQLdb()

app = Flask(__name__)
engine = create_engine(f'mysql://{username}:{password}@{host}:{port}/{database}')
conn = engine.connect()

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/form')
def forms():

    return render_template('form.html')

@app.route('/api/data/nova_listings')
def nova_listings():
    conn = engine.connect()
    query = '''
        SELECT * FROM nova_listings
    '''
    results_df = pd.read_sql(query, con=conn)
    results_json = results_df.to_json(orient='records')
    conn.close()
    return results_json

@app.route('/api/data/city_type_price')
def city_type_price():
    conn = engine.connect()
    query = '''
        SELECT
            `PROPERTY TYPE` AS PropertyType
            ,CITY AS City
            ,AVG(PRICE) AS AveragePrice
        FROM
            nova_listings
        GROUP BY
            `PROPERTY TYPE`
            , CITY
        ORDER BY 
            AVG(PRICE) DESC
    '''
    results_df = pd.read_sql(query, con=conn)
    results_json = results_df.to_json(orient='records')
    conn.close()
    return results_json

@app.route('/api/data/property_type_price')
def property_type_price():
    conn = engine.connect()
    single_family_query = '''
        SELECT
            `CITY`
            ,AVG(PRICE)
        FROM
            nova_listings
        WHERE
            `PROPERTY TYPE` = 'Single Family Residential'
        GROUP BY
            `CITY`
        '''
    single_family_df = pd.read_sql(single_family_query, con=conn)
    condo_query = '''
        SELECT
            `CITY`
            ,AVG(PRICE)
        FROM
            nova_listings
        WHERE
            `PROPERTY TYPE` IN ('Condo/Co-op')
        GROUP BY
            `CITY`
        '''
    condo_df = pd.read_sql(condo_query, con=conn)
    townhouse_query = '''
        SELECT
            `CITY`
            ,AVG(PRICE)
        FROM
            nova_listings
        WHERE
            `PROPERTY TYPE` IN ('Townhouse')
        GROUP BY
            `CITY`
        '''
    townhouse_df = pd.read_sql(townhouse_query, con=conn)
    single_family_condo_df = pd.merge(single_family_df, condo_df, on='CITY', how='outer')
    single_family_condo_df.rename(columns={
        'CITY':'City'
        ,'AVG(PRICE)_x':'SingleFamilyAvgPrice'
        ,'AVG(PRICE)_y':'CondoAvgPrice'
    }, inplace=True)
    single_family_condo_townhouse_df = pd.merge(single_family_condo_df, townhouse_df, left_on='City', right_on='CITY', how='outer')
    single_family_condo_townhouse_df.rename(columns={
        'AVG(PRICE)':'TownhouseAvgPrice'
    }, inplace=True)
    single_family_condo_townhouse_df['City'].fillna(single_family_condo_townhouse_df['CITY'], inplace=True)
    del single_family_condo_townhouse_df['CITY']
    single_family_condo_townhouse_df
    single_family_condo_townhouse_json = single_family_condo_townhouse_df.to_json(orient='records')
    conn.close()

    return single_family_condo_townhouse_json


@app.route("/send", methods=["GET", "POST"])
def send():
    conn = engine.connect()
    if request.method == "POST":
        sale_type = request.form['saleType']
        sold_date = request.form['soldDate']
        property_type = request.form["propertyType"]
        property_address = request.form["homeAddress"]
        city = request.form["homeCity"]
        state = request.form["homeState"]
        zip_code = request.form["homeZipCode"]
        price = request.form['homePrice']
        beds = request.form['beds']
        baths = request.form['baths']
        location = request.form['location']
        square_feet = request.form["homeSquareFeet"]
        lot_size = request.form['lotSize']
        year_built = request.form['yearBuilt']
        days_in_market = request.form['DaysInMarket']
        price_per_square_feet = request.form['PricePerSquareFeet']
        hoa = request.form['HOA']
        status = request.form['status']
        open_house_start_time = request.form['openHouseStart']
        open_house_closing_time = request.form['openHouseClosing']
        url = request.form['URL']
        source = request.form['source']
        mls = request.form['MLS']
        favorite = request.form['Favorite']
        interested = request.form['interested']
        latitude = request.form['LAT']
        longitude = request.form['LON']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone = request.form['phone']
        home_df = pd.DataFrame({
            'SALE TYPE': [sale_type],
            'SOLD DATE': [sold_date],
            'PROPERTY TYPE': [property_type],
            'ADDRESS': [property_address],
            'CITY': [city],
            'STATE OR PROVINCE': [state],
            'ZIP OR POSTAL CODE': [zip_code],
            'PRICE': [price],
            'BEDS': [beds],
            'BATHS': [baths],
            'LOCATION': [location],
            'SQUARE FEET': [square_feet],
            'LOT SIZE': [lot_size],
            'YEAR BUILT':[year_built],
            'DAYS ON MARKET':[days_in_market],
            '$/SQUARE FEET': [price_per_square_feet],
            'HOA/MONTH': [hoa],
            'STATUS': [status],
            'NEXT OPEN HOUSE START TIME': [open_house_start_time],
            'NEXT OPEN HOUSE END TIME': [open_house_closing_time],
            'URL': [url],
            'SOURCE': [source],
            'MLS#': [mls],
            'FAVORITE': [favorite],
            'INTERESTED': [interested],
            'LATITUDE': [latitude],
            'LONGITUDE': [longitude],
            'FIRST NAME': [first_name],
            'LAST NAME': [last_name],
            'PHONE': [phone]
        })
        home_df.to_sql('nova_listings', con=conn, if_exists='append', index=False)

        #return redirect("/", code=302)

    conn.close()

    return render_template("form.html")

@app.route('/julia')
def julia():
    return render_template("julia.html")
if __name__ == '__main__':
    app.run(debug=True)