
# 🏥 HOSTOBOT
## 🚀DEMO LLM RAG with LangChain and GEMINI or OPENAI models


<div align="center">

<img src="https://img.freepik.com/vecteurs-libre/gens-qui-marchent-assis-au-batiment-hopital-exterieur-verre-clinique-ville-illustration-vectorielle-plane-pour-aide-medicale-urgence-architecture-concept-soins-sante_74855-10130.jpg?semt=ais_hybrid&w=740&q=80"/>
  
| Neo4j | Gemini | OpenAI |
| :---: | :---: | :---: |
| <img src="https://miro.medium.com/0*4u0EbR8ZDo48DqF-.jpeg" width="150"> | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/1280px-Google_Gemini_logo.svg.png" width="150"> | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/OpenAI_Logo.svg/960px-OpenAI_Logo.svg.png" width="150"> |

</div>


Using an **Agentic Microservices Architecture** 🏗️, this is a **showcase** of a **LangChain Agent** 🧠 based on a **LLM and a list of tools** to access **Graph RAG** data (Neo4j) 🕸️ + MiddleBack/ETL (Python) 🐍 about requesting in natural language hospital data.

## ⚙️ Configuration
To be able to run the application, you only need to have:
- 🔑 NEO4J IDs (URI, Username, Password)
- 🔑 An OpenAI or Gemini API Key

**📝 Action: Fill the .env file and ensure Docker Desktop 🐳 is running before executing the commands.**


## 🛠️ To run the application
>>> docker compose up --build

## 🌐 Local Access points
Once the containers are healthy, access the following interfaces:
- 📖 API Documentation (FastAPI): http://localhost:8000/docs
- 💬 Chatbot Interface (Streamlit): http://localhost:8501/

## ❓ Example Questions

- Which hospitals are part of the hospital network?
- What’s the current wait time at Wallace-Hamilton Hospital?
- At which hospitals are patients reporting issues related to billing or insurance?
- What’s the average length in days for completed emergency visits?
- How are patients describing the nursing team at Castaneda-Hardy?
- What was the total amount billed to each payer during 2023?
- What is the average charge for visits covered by Medicaid?
- Which doctor has the shortest average visit duration?
- What is the total billed amount for patient 789's hospital stay?
- Which state saw the biggest percentage increase in Medicaid visits from 2022 to 2023?
- What’s the average daily billing amount for patients with Aetna coverage?
- How many patient reviews have been submitted from Florida?
- For visits that include a chief complaint, what percentage also have a review?
- What percentage of visits at each hospital include patient reviews?
- Which physician has received the highest number of reviews for their visits?
- What is the unique identifier for Dr. James Cooper?
- Show all reviews associated with visits handled by physician 270 — include every one.
