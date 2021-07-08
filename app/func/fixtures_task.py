from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.expression import update
from app.models import *
from app.func import bp
from .celery import celery
from app import db
import app
import json
import sqlite3
import requests
import datetime

#con = sqlite3.connect('app.db')#connection object to access the data base

#@celery.task
def gen_fixtures():
    app.models.Fixtures.query.delete()
    # THIS SECTION OF FIXTURES FUNCTION GRABS DATA FROM API AND PLACES IN JSON FILE TO BE USED IN THE REST OF THE FUNCTION
    url = "https://fantasy.premierleague.com/api/fixtures/"#CHECK POST MAN FOR DATA DIFFERENTIATION
    general_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

    response = requests.request("GET", url)
    general_req = requests.request("GET", general_url)

    fpl = response.json()
    general = general_req.json()

    #DECLARATION OF VARIABLES WHICH WILL BE USED THROUGHOUT
    count = 0
    daily = {}
    gameweek = 0

    #THIS FINDS THE CURRENT GAMEWEEK OF THE PREMIER LEAGUE
    for gw in general['events']:
        if gw ['is_current'] == True:
            gameweek = gw['id']
        elif gw ['is_next'] == True and gameweek == 0:
            gameweek = gw['id']

    

    #THIS FINDS EACH FIXTURE FOR THIS GAME WEEK AND PLACES THEM IN A DICTIONARY 
    for fixtures in fpl:
        if fixtures['event'] == gameweek:
            home_code = fixtures['team_h']
            away_code = fixtures['team_a']
            if fixtures['team_h_score'] == None:
                home_score = 0
            else:
                home_score = fixtures['team_h_score']
            if fixtures['team_a_score'] == None:
                away_score = 0
            else:
                away_score = fixtures['team_a_score']
    
            for team in general["teams"]:
                if home_code == team["id"]:
                    home_team = team["name"]
            for team in general["teams"]:
                if away_code == team["id"]:
                    away_team = team["name"]

        else:
            continue    
        daily[count] = [home_team,home_score,away_score,away_team]
        count+=1

    #THIS FOR LOOP ADDS EACH FIXTURE IN THE DICTIONARY TO THE DATABASE
    for fixtures in range(0,len(daily)):
        new_fixture = Fixtures(home = daily[fixtures][0], home_score = daily[fixtures][1], away = daily[fixtures][3], away_score = daily[fixtures][2])
        db.session.add(new_fixture)
        db.session.commit()
    
    '''for fixtures in range(len(daily)):
        for details in daily[x]:
            new_fixture = Fixtures(home = details[0], home_score = details[1], away = details[3], away_score = details[2])
            db.session.add(new_fixture)
            db.session.commit()'''

    '''#THIS LOOP CHECKS IF THE GAME WEEK IS OVER TO DELETES ALL FIXTURES FROM THIS GAME WEEK 
    FIND A WAY TO PLACE NEW FIXTURES ABOVE THE OLD ONES ADD GW AS A ROW IN FIXTURE TABLE MAKE PROGRAM ONLY DISPLAY THESE FIXTURES
    for check in general['events']:
        if check['id'] == gameweek:
            if check['finished'] == True:
                try:
                    num_rows_deleted = db.session.query(Fixtures).delete()
                    db.session.commit()
                except:
                    db.session.rollback()'''
    
    #THIS PROCESS UPDATES THE SCORES IN REAL TIME
    '''cursor = db.cursor()
    fixture_id = cursor.execute('SELECT COUNT(*) FROM Fixtures')
    
    for fix_id in range (1,fixture_id+1):
        cursor.execute(UPDATE Fixtures  SET home_score = ?, away_score = ? WHERE id = ? ,
        (daily[fix_id][1], daily[fix_id][2], fix_id))
        db.commit()'''
    for fix_id in range(1,len(daily)+1):
        dict_check = 0
        update_fixture = Fixtures.query.filter_by(id = fix_id).first()
        update_fixture.home_score = daily[dict_check][1]
        update_fixture.away_score = daily[dict_check][2]
        db.session.commit()

        '''db.session.query(Fixtures)\
            .filter_by(id = fix_id).first()\
                .update(home_score = daily[fix_id][1], away_score = daily[fix_id][2])'''



@bp.route('/fixtures', methods = ['GET','POST'])
def fixture():
    gen_fixtures()
    fixtures = Fixtures.query.all()
    return render_template('func/fixtures.html', fixtures = fixtures)


    
    


