"""
Health Checker
:Version: 1.0
:Authors: Max Van De Ven, Pauline Schudrowitsch, Sarah Stein
"""


### PREREQUISITES##########################################################################################
# import of required libraries


import streamlit as st #web app
from streamlit_option_menu import option_menu #menu option
from PIL import Image #image display
import pandas as pd #data manipulation
import xml.etree.ElementTree as ET #https://docs.python.org/3/library/xml.etree.elementtree.html
from datetime import date, datetime, timedelta as td
import pytz
import json
import numpy as np #random number generation
import urllib #for url links ###BRAUCHEN WIR DAS WIRKLICH?


### APP FUNCTION############################################################################################
def healthchecker():
    """Health Checker"""


    ### definition of icon and name of web-app tab#####################
    st.set_page_config(
        page_title= "HealthTracker",
        page_icon="assets/logo_small_png.png",
        layout="wide",
        initial_sidebar_state="expanded")
 #CSS to make contact form pretty
    with open ("style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    ### menu###########################################################
    #https://www.youtube.com/watch?v=hEPoto5xp3k
    #icons automatically taken from https://icons.getbootstrap.com/
    with st.sidebar:
        logo = Image.open("assets/logo_cut_png.png")             
        st.image(
            logo,
            caption=None,
            width=300,
            use_column_width=None,
            clamp=False,
            channels="RGB",
            output_format="auto")
        selected = option_menu(
            menu_title=None, #required
            options=["Home", "Detailed Metric View", "User Profile", "Contact"], #required
            icons=["house", "zoom-in", "person", "envelope"], #optional
            menu_icon="list", #optional
            default_index=0, #optional, defines which page should be shown when opening the webpage
        )


##################################################################


    ###
    # PLATZHALTER ODER HILFSVARIABLEN --> SPÄTER ANZUPASSEN AN GEGEBENEN INPUT
    first_name = "Jane"
    last_name="Smith"
    dailystep_goal = 10000
    dailyactivecalories_goal = 400
    dailystandgoal= 12
    dailyexercisegoal= 30
    ###


    ### DATA IMPORT FEATHER-FORMAT#################################

    # data import
    data = pd.read_feather("data/export_conv.ftr")

    # add new column date with cleaned date format based on input of endDate column
    data["date"] = data["endDate"].dt.strftime("%Y-%m-%d")


    # filter StepCount data per day
    stepcount = data[data["type"] == "StepCount"]
    dated_stepcount = stepcount.groupby("date").agg(["sum"])    
    last_stepcount = int(dated_stepcount.iloc[-1,[4]])
    prelast_stepcount = int(dated_stepcount.iloc[-2,[4]])

    # filter basal energy burned per day
    basalenergy = data[data["type"] == "BasalEnergyBurned"]
    dated_basalenergy = basalenergy.groupby("date").agg(["sum"])
    last_basalenergy = int(dated_basalenergy.iloc[-1,[4]])
    prelast_basalenergy = int(dated_basalenergy.iloc[-2, [4]])

    # filter active energy burned per day
    activeenergy = data[data["type"] == "ActiveEnergyBurned"]
    dated_activeenergy = activeenergy.groupby("date").agg(["sum"])
    last_activeenergy = int(dated_activeenergy.iloc[-1,[4]])
    prelast_activeenergy = int(dated_activeenergy.iloc[-2, [4]])
    
    # filter exercise time per day
    exercisetime = data[data["type"] == "AppleExerciseTime"]
    dated_exercisetime = exercisetime.groupby("date").agg(["sum"])
    last_exercisetime = int(dated_exercisetime.iloc[-1,[4]])
    prelast_exercisetime = int(dated_exercisetime.iloc[-2, [4]])

    # filter stand hours per day
    standhours = data[data["type"] == "AppleStandHour"]
    dated_standhours = standhours.groupby("date").agg(["sum"])
    last_standhours = int(dated_standhours.iloc[-1,[4]])
    prelast_standhours = int(dated_standhours.iloc[-2, [4]])

     # filter average heartrate per day
   # heartrate = data[data["type"] == "HeartRate"]
   # dated_heartrate = heartrate.groupby("date").agg(["mean"])
   # last_avgheartrate = int(dated_heartrate.iloc[-1,[3]])
   # prelast_avgheartrate = int(dated_heartrate.iloc[-2, [3]])

    # filter minimum heartrate per day
   # dated_minheartrate = heartrate.groupby("date").agg(["min"])
   # last_minheartrate = int(dated_minheartrate.iloc[-1,[7]])
   # prelast_minheartrate = int(dated_minheartrate.iloc[-2, [7]])

    # filter maximum heartrate per day
    #dated_maxheartrate = heartrate.groupby("date").agg(["max"])
    #last_maxheartrate = int(dated_maxheartrate.iloc[-1,[7]])
    #prelast_maxheartrate = int(dated_maxheartrate.iloc[-2, [7]])

    # receive weight data
    weight = data[data["type"] == "BodyMass"]
    dated_weight = weight.groupby("date").agg(["sum"])
    last_weight = int(dated_weight.iloc[-1,[4]])
    prelast_weight = int(dated_weight.iloc[-2, [4]])
    
    # get height (in meter) of user --> DATEN NOCH ZU FINDEN IN DATENSET
    height = 1.70

    
    ### Content of Home Page###########################################  
    if selected == "Home":
        st.title(f"Hi {first_name}!")
        with st.container():
            if int(prelast_weight//(height**2)) > 25:
                st.write("You are slightly overweight, try exercising more.")
            #if int(last_avgheartrate-prelast_avgheartrate) > 140:
                st.write("Your average heartrate is extremely high, consider contacting your general practitioner for a follow up.")
            #elif int(last_avgheartrate-prelast_avgheartrate) > 100 and int(last_avgheartrate-prelast_avgheartrate) < 120 and int(last_exercisetime-prelast_exercisetime) < 45: #High avg HR but low exercise time can be a signal for increased stress#
                st.write("Your average heartrate is considerably increased. \n This can be an indicator of stress. \n Here are some informational videos about stress: \n <insert YT links>")
            #elif int(last_minheartrate-prelast_minheartrate) > 85:
                st.write("Your low heart rate is high compared to the general average. \n Consider increasing your cardiovascular fitness. \n Below are some informational videos about cardio exercises: \n <insert YT links>")
            #elif int(last_maxheartrate-prelast_maxheartrate) > 188:
                st.write("Your maximum heart rate exceeded the average maximum for your age. \n Try reducing your maximum heart rate by performing low intensity cardio.")
            
            elif int(last_stepcount-prelast_stepcount) < 1000 and int(last_exercisetime-prelast_exercisetime) < 10:
                st.write("You have not yet performed any activity today. Consider going for a walk to get the blood flowing.")
            elif int(last_stepcount-prelast_stepcount) > 10000 and int(last_exercisetime-prelast_exercisetime) > 60 and int(last_activeenergy-prelast_activeenergy) > 750:
                st.write("You have reached your activity goals for today, keep up the good work!")
            elif int(last_stepcount-prelast_stepcount) < 5000 and int(last_standhours-prelast_standhours) < 4:
                st.write("You have spent a great amount of time seated. Consider going for a walk to reach your daily activity goals.")
            else:
                st.write("Your vitals seem healthy and you reached all your goals. \n Keep up the good work!")
       
       
        with st.container():
            #TO DO: Insert Health Analysis
            st.subheader("PLATZHALTER CONTAINER: Here we will add the analysis and short description of the user's health.")
        st.write("##")

        ### KPI Container###########################
        with st.container():
            st.write("----")
            st.write("Heart & Weight Data")
           
            metric1, metric2, metric3, metric4, metric5, metric6, metric7 = st.columns(7) #5 columns and metrics

            ### KPI ONE#####################
           # with metric1:
               # metric1.metric(label = "Average Heart Rate",
                  #             value = last_avgheartrate,
                  #             delta = (last_avgheartrate--prelast_avgheartrate),
                  #             delta_color = "inverse")
        
            ### KPI: Minimum Heart Rate##################### 
       #     with metric2:
        #        metric2.metric(label = "Minimum Heart Rate",
        #                       value = last_minheartrate,
        #                       delta = (last_minheartrate-prelast_minheartrate),
         #                      delta_color = "inverse")

            ### KPI: Maximum Heart Rate##################### 
      #      with metric3:
      #          metric3.metric(label = "Maximum Heart Rate",
      #                         value = last_maxheartrate,
     #                          delta = (last_maxheartrate-prelast_maxheartrate),
#                               delta_color = "inverse")

            ### KPI: Weight#####################
            with metric4:
                metric4.metric(label = "Weight (kg)",
                                value = last_weight,
                                delta = (last_weight - prelast_weight),
                                delta_color = "inverse")

            ### KPI: BMI#####################
            with metric5:
                metric5.metric(label = "BMI",
                                value = int(last_weight//(height**2)),
                                delta = int(prelast_weight//(height**2)),
                                delta_color = "inverse")
        with st.container():
            st.write("###")
            st.subheader("Movement Data")
                
            metric6, metric7, metric8, metric9, metric10 = st.columns(5) #5 columns and metrics

            ### KPI: Step Count####################
            with metric6:
                metric6.metric(label = "Step Count",
                               value = last_stepcount,
                               delta = (last_stepcount-prelast_stepcount))

            ### KPI: Stand Hours####################
            with metric7:
                metric7.metric(label = "Stand Hours of 24",
                               value = last_standhours,
                               delta = (last_standhours-prelast_standhours))

            ### KPI: Exercise Time#####################
            with metric8:
                metric8.metric(label = "Exercise Time (min)",
                               value = last_exercisetime,
                               delta = (last_exercisetime-prelast_exercisetime))
                
            ### KPI: Basal Energy Burned#####################
            with metric9:
                metric9.metric(label = "Basal Energy Burned (kcal)",
                               value = last_basalenergy,
                               delta = (last_basalenergy-prelast_basalenergy))
                

            ### KPI: Active Energy Burned#####################
            with metric10:
                metric10.metric(label = "Active Energy Burned (kcal)",
                                value = last_activeenergy,
                                delta = (last_activeenergy-prelast_activeenergy))
                
            st.write("----")


    ###Content of Detailed Metric View Page########################################
    if selected == "Detailed Metric View":
        st.title("Detailed Metric View")
        st.subheader(f" Hi {first_name}! Here is an overview about your metrics.")

        metric_selection = st.selectbox(
            "Which parameter do you want to analyze in detail?",
            ("Select","Step Count", "Exercise Time", "Active Calories", "Hours Stood", "Minimum Heartrate"))

        with st.container():
            if metric_selection == "Select":
                st.write("Please select a metric to be displayed.")
            #if metric_selection == "Step Count":
            #  df=pd.DataFrame(
            #      np-random.randn(10, 2),
            #      columns=["day", "steps"])
           # st.line_chart(df)
              
              
              #  metric_labels_1={"dailystep_goal": "Daily step goal", "last_stepcount": "Last Step Count"}
           #     stepcount_chart= f"{metric_labels_1
                #[dailystep_goal]}"
              #  fig= px.line()
            if metric_selection == "Step Count":
                if last_stepcount>= dailystep_goal:
                    st.write(f"Good job! Your goal is walking {dailystep_goal} steps a day. You beat your goal and took {last_stepcount} steps today! :shoe:")
                else:
                 st.write(f"Your goal is walking {dailystep_goal} steps a day. Try walking a little more, since your count is {last_stepcount} for today :shoe: ")

            if metric_selection == "Exercise Time":
                if last_exercisetime>= dailyexercisegoal:
                    st.write(f"Good job! Your exercise goal has been reached! You have exercised {last_exercisetime} minutes today, {first_name} :thumbsup:")
                else:
                    st.write(f"It seems like you did not reach your exercise goal today by exercising {last_exercisetime} minutes from {dailyexercisegoal} minutes. Maybe you will manage to squeeze in a little workout today?")
                #dated_stepcount = stepcount.groupby("date").agg(["sum"]).plot.line(legend=True,subplots=False)
                
    # st.line_chart(dated_stepcount)
            if metric_selection == "Active Calories":
                if last_activeenergy >= dailyactivecalories_goal:
                    st.write(f"Good job, {first_name}! :fire: Your goal is burning {dailyactivecalories_goal} active calories a day. You beat your goal and burnt {last_activeenergy} calories today!")
                else:
                    st.write((f"Your goal is burning {dailyactivecalories_goal} active calories a day. Try moving a little more, since your count is {last_activeenergy} active calories today."))
            if metric_selection == "Hours Stood":
                if last_standhours >= dailystandgoal:
                    st.write(f"Your goal is standing at least one minute per hour. Good job, you stood for at least a minute for {last_standhours} hours today. You beat your goal of {dailystandgoal} steps today!")
                else:
                    st.write((f"Your goal is standing at least one minute for {dailystandgoal} hours. Try moving a little bit more, since your count is {last_standhours} for today."))
                    avg_standhours_df = standhours_df.groupby(by=["StandHours"]).mean()
                    #avg_standhours_df

                    bar_fig= avg_standhours_df[["StandHours"]].iplot(kind="bar",
                    barmode="stack",
                    yTitle="Stand Hours",
                    title="Stand Hours",
                    asFigure= True,
                    opacity=1.0)
                    #st.bar_chart(data=last_standhours, width = 0, height= 0, use_container_width= True)
                   # st.bar_chart(standhours_df.groupby("StandHours"))
                   #,etric= st.sidebar.radio("Choose a metric to compare")
                   # standhours.groupby("date").mean()

           # if metric_selection=="Minimum Heartrate":
                #st.write("THe heart rate measures the number of times the heart beats per minute. Resting heartrates can differ by age.")
                    ####!!!!CODE NEEDED
           
        


    ###Content of User Profile Page################################################               
    if selected == "User Profile":
        st.title("Here is an overview of your User Profile")
        with st.container():
            st.write(f"Your first name is {first_name}. Your last name is {last_name}.")
        
       # first_name = st.text_input("What is your first name?", "")
        #gender = st.selectbox(
         #   "How do you identify?",
       #     ("Male", "Female", "Other"))
      #  age = st.slider("How old are you?",0,120,25)
      #  height = st.slider("How tall are you?", 0, 250, 170)



    ###Content of Contact Page#####################################################
    if selected == "Contact":
        st.title("Got Questions or Suggestions?")
        st.subheader("Tell us :mailbox:")
        with st.container(): 
            st.write("##")
            
            #Contact Form Functionality########################
            #https://www.youtube.com/watch?v=FOULV9Xij_8
            #https://formsubmit.co/?utm_source=formsubmit.co&utm_medium=site%20link&utm_campaign=submission%20page
            #https://www.w3schools.com/howto/howto_css_contact_form.asp
            #Filled out contact form will be sent to HealthTracker (in this case Pauline´s Nova Student email address) 
            contact_form= """ 
            <form action="https://formsubmit.co/48981@novasbe.pt" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder= "Your Name" required> 
                <input type="email" name="email" placeholder= "Your Email" required> 
                <textarea name ="message" placeholder="Please write your message here" required style="height:200px; width:540px"></textarea> 
                <button type="submit">Send</button> 
            </form> 
            """ 

            #inject code into Webapp  
            left_column, right_column= st.columns(2) 

            with left_column: 
                st.markdown(contact_form, unsafe_allow_html=True)
            with right_column: 
                st.empty()

      


            st.write("##")
            st.write("##")
            st.write("##")
            st.write("##")
            expander = st.expander("Imprint", expanded= False)
            with expander:
                st.info("This project was created as a project part of the Introduction to Programming course by Sarah Stein, Max van de Ven, and Pauline Schudrowitsch at Nova SBE.")


###APP ####################################################################################################
healthchecker()

