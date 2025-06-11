# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Text, Dict, List

import arrow 
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

import mysql.connector

connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root", 
        password="",
        database='anime'
    )

def fetchAnime(genre, rating, episodes, category):
    
    cursor = connection.cursor(buffered=True)
    # # Connection test
    # if connection.is_connected():
    #     return f"Connected"
    # else:
    #     return "failed"
    if genre:
        if len(genre) == 1:
            sql = """SELECT * FROM anime WHERE FIND_IN_SET(%s, genre) ORDER BY rating DESC""" 
            tuple = (genre[0],)
            
        elif len(genre) == 2:  
            sql = """SELECT * FROM anime WHERE FIND_IN_SET(%s, genre) AND FIND_IN_SET(%s, genre) ORDER BY rating DESC"""
            tuple = (genre[0], genre[1])
        
        elif len(genre) == 3:  
            sql = """SELECT * FROM anime WHERE FIND_IN_SET(%s, genre) AND FIND_IN_SET(%s, genre) AND FIND_IN_SET(%s, genre) ORDER BY rating DESC"""
            tuple = (genre[0], genre[1], genre[2])
            
        else:
            sql = """SELECT * FROM anime WHERE FIND_IN_SET(%s, genre) AND FIND_IN_SET(%s, genre) AND FIND_IN_SET(%s, genre) ORDER BY rating DESC"""
            tuple = (genre[0], genre[1], genre[2])
            
    elif rating:
        if episodes:
            if category:
                sql = """SELECT * FROM anime WHERE rating <= %s AND episodes = %s AND type = %s"""
                tuple = (rating,episodes,category)
            else:
                sql = """SELECT * FROM anime WHERE rating <= %s AND episodes = %s"""
                tuple = (rating,episodes)
        elif category:
            sql = """SELECT * FROM anime WHERE rating <= %s AND type = %s"""
            tuple = (rating,category)
        else:        
            sql = """SELECT * FROM anime WHERE rating <= %s"""
            tuple = (rating,)
        
    elif episodes:
        sql = """SELECT * FROM anime WHERE episodes = %s"""
        tuple = (episodes,)
    
    elif category:
        sql = """SELECT * FROM anime WHERE type = %s"""
        tuple = (category,)
        
    try:
        #Execute the SQL Query
        if genre:
            if rating:
                cursor.execute(sql,tuple) 
                result = cursor.fetchall()
                if episodes:
                    if category:
                        for x in result:
                            if x[5] <= rating and x[4] == episodes and x[3] == category:
                                rs = x
                                break
                    else:
                        for x in result:
                            if x[5] <= rating and x[4] == episodes:
                                rs = x
                                break
                elif category:
                    for x in result:
                        if x[5] <= rating and x[3] == category:
                            rs = x
                            break  
                else:
                    for x in result:
                        if x[5] <= rating:
                            rs = x
                            break
            elif episodes:
                cursor.execute(sql,tuple) 
                result = cursor.fetchall()
                for x in result:
                    if x[4] == episodes:
                        rs = x
                        break
            elif category:
                cursor.execute(sql,tuple) 
                result = cursor.fetchall()
                for x in result:
                    if x[3] == category:
                        rs = x
                        break
            else:
                cursor.execute(sql,tuple) 
                rs = cursor.fetchone()
        else:
            cursor.execute(sql,tuple) 
            rs = cursor.fetchone()
        
        cv = float(rs[5])
        new  = cv-0.01
        newRating= str(new)
        
        msg = f"I would recommend this anime: {rs[1]}.\nThe genres are {rs[2]}.\nIt is an {rs[3]} anime with {rs[4]} episodes and have {rs[5]} rating"
                
        #Now print fetched data
        return msg, newRating

    except:
        return f"ERROR : Unable to fetch data (Consider entering another request)"
    
class ActionFetchAnime(Action):

    def name(self) -> Text:
        return "action_fetch_anime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # genre = next(tracker.get_latest_entity_values("genre"), None)
        genre = tracker.get_slot("genre")
        rating = next(tracker.get_latest_entity_values("rating"), None)
        episodes = next(tracker.get_latest_entity_values("episodes"), None)
        category = next(tracker.get_latest_entity_values("category"), None)
        if category == "movie":
            category = "Movie"
        
        SlotSet("REMgenre", genre)
        SlotSet("REMepisodes", episodes)
        SlotSet("REMcategory", category)
        
        msg, newRating = fetchAnime(genre, rating, episodes, category)
        dispatcher.utter_message(text=msg)
        
        
        return [
            SlotSet("REMgenre", genre),
            SlotSet("REMepisodes", episodes),
            SlotSet("REMcategory", category),
            SlotSet("REMrating", newRating),
            SlotSet("genre", None),
            SlotSet("rating",None),
            SlotSet("episodes",None),
            SlotSet("category",None),
            ]

class ActionFetchAnotherAnime(Action):

    def name(self) -> Text:
        return "action_fetch_another_anime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # genre = next(tracker.get_latest_entity_values("genre"), None)
        genre = tracker.get_slot("REMgenre")
        rating = tracker.get_slot("REMrating")
        episodes = tracker.get_slot("REMepisodes")
        category = tracker.get_slot("REMcategory")
        
        NEWgenre = tracker.get_slot("genre")
        if NEWgenre:
            genre = NEWgenre
            
        NEWrating = next(tracker.get_latest_entity_values("rating"), None)
        if NEWrating:
            rating = NEWrating
            
        NEWepisodes = next(tracker.get_latest_entity_values("episodes"), None)
        if NEWepisodes:
            episodes = NEWepisodes
            
        NEWcategory = next(tracker.get_latest_entity_values("category"), None)
        if NEWcategory:
            category = NEWcategory
        
        msg, newRating = fetchAnime(genre, rating, episodes, category)
        dispatcher.utter_message(text=msg)
        
        
        return [
            SlotSet("REMgenre", genre),
            SlotSet("REMepisodes", episodes),
            SlotSet("REMcategory", category),
            SlotSet("REMrating", newRating),
            SlotSet("genre", None),
            SlotSet("rating",None),
            SlotSet("episodes",None),
            SlotSet("category",None),
            ]