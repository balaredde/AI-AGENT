
This project is about a intelligent agent that was built by using Google ADK(agent development kit )

the dependecies were present in requirements.txt 
pip install -r requirements.txt

create a virtual env in base directory

the Google adk follows a certain code structure
in the base directory u need create seperate folder for each agent you want to build 

get the api from google cloud and paste it in .env

# TO RUN 
.venv\Scripts\activate
adk web

a web UI is shown


AI/
│
├── test_agent/
    |──agent.py                  # agent
    |──.env                      #contains google api
    |── requirements.txt

the agent.py should contain root_agent which will be automatically recognized by adk

you can run the web ui by using the command adk web  "make sure that the Scripts are activated"

#data handling 

1) i have changes the column name to avoid key error 

2) the excel file is loaded in a pandas data frame in string format , cause its taking 02 as 2 

3) ! MAIN POINT  as agents understand dict very well , i converted data frame into a dictionary 


# agent's architecture

A class is defined as HSN agent 

creates a agent named test_agent , we use gemini-1.5-flash model  

the handle func takes the prompt from the user and proccess it 

1) our target is to extract the list of code or codes from the user prompt if the user didnt enter 
any numerical values it says to enter any HSN code--> "re.findall(r'\b\d+\b', prompt)"

2) next we validate the code length , in most of the cases they were present between 2 to 8 
we extracted min max values from excel for reference  , if the code length is inappropiate its asks to enter a valid code

3) returns description or chapter name by checking if the code is present in the hsn_dict else data  not found

4) it validates for all the codes present in the list

5) class DescriptionOutput(BaseModel)  used to standardize the agent’s response.

6) after creating a agent object it automatically calls handle function 


