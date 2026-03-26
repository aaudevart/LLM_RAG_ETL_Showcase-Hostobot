# 🏥 HOSTOBOT

<div align="center">
  <img src="https://img.freepik.com/vecteurs-libre/gens-qui-marchent-assis-au-batiment-hopital-exterieur-verre-clinique-ville-illustration-vectorielle-plane-pour-aide-medicale-urgence-architecture-concept-soins-sante_74855-10130.jpg?semt=ais_hybrid&w=740&q=80" alt="Hospital Concept" width="400" />
</div>

<br>

<div align="center">

| LangChain | Neo4j | Gemini | OpenAI | MistralAI |
| :---: | :---: | :---: | :---: | :---: |
| <img src="https://cdn.brandfetch.io/idzf7Sjo28/w/800/h/184/theme/dark/id12EQi2QW.png?c=1bxid64Mup7aczewSAYMX&t=1773104478968" width="130" alt="LangChain"> | <img src="https://dist.neo4j.com/wp-content/uploads/20230926084108/Logo_FullColor_RGB_TransBG.svg" width="100" alt="Neo4j"> | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/1280px-Google_Gemini_logo.svg.png" width="80" alt="Gemini"> | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/OpenAI_Logo.svg/960px-OpenAI_Logo.svg.png" width="80" alt="OpenAI"> | <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMTH6AVMJcaD1iKlj-L6Tw36jjd1x403Nb_Q&s" width="90" alt="MistralAI"> |

</div>

<br>

## 🚀 Overview

**HOSTOBOT** is an **Agentic Microservices Architecture** 🏗️ that serves as a showcase of a Multi-Agent System using **LangChain Agents** 🧠. By connecting a Large Language Model (LLM) with a set of powerful, specialized tools, it interacts with a **Graph RAG** database (Neo4j) 🕸️ and a MiddleBack/ETL pipeline written in Python 🐍.

This platform empowers users to effortlessly request complex hospital-related data using natural language queries.

---

## 🏗️ Architecture

The intelligent core of this system is the **🏥 Hospital RAG Agent**, which dynamically routes queries using the following advanced tools:

- 🛠️ **Current Hospitals** (`get_current_hospitals_tools`) — Retrieves the active list of hospitals directly from the Neo4j database.
- 🛠️ **Wait Times** (`get_current_wait_times`) — Generates a simulated current wait time for patient emergency visits.
- 🛠️ **Most Available Hospital** (`get_most_available_hospital`) — Suggests the most optimal hospital with the highest available capacity.
- 🔗🛠️ **Experiences & Reviews** (`get_reviews`) — Leverages Vector Search capabilities on patient "Review" nodes via a `Neo4jVectorSearchChain`, seamlessly integrating qualitative semantic search into the populated graph database.
- 🔗🛠️ **Graph Querying** (`get_graph`) — Dynamically translates natural language questions into precise Cypher queries using a `CypherChain`, enabling direct quantitative question-answering against the complex graph structure.

---

## ⚙️ Configuration

To run the application, you need the following prerequisites:

- 🔑 **NEO4J Credentials**: URI, Username, and Password.
- 🔑 **AI API Key**: Choose between OpenAI, Gemini, or Mistral.

> **📝 Action:** Provide these credentials in your `.env` file and ensure **Docker Desktop 🐳** is running before proceeding.

---

## 🛠️ Installation & Execution

Start the entire microservices stack with a single command:

```bash
docker compose up --build
```

### 🌐 Local Access Points

Once the Docker containers are built and healthy, you can access the localized services:

- 📖 **API Documentation (FastAPI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 💬 **Chatbot UI (Streamlit)**: [http://localhost:8501/](http://localhost:8501/)

---

## ❓ Example Questions to Ask

Try testing the agent with some of these complex, natural language questions:

- *Which hospitals are part of the hospital network?*
- *What’s the current wait time at Wallace-Hamilton Hospital?*
- *At which hospitals are patients reporting issues related to billing or insurance?*
- *What’s the average length in days for completed emergency visits?*
- *How are patients describing the nursing team at Castaneda-Hardy?*
- *What was the total amount billed to each payer during 2023?*
- *What is the average charge for visits covered by Medicaid?*
- *Which doctor has the shortest average visit duration?*
- *What is the total billed amount for patient 789's hospital stay?*
- *Which state saw the biggest percentage increase in Medicaid visits from 2022 to 2023?*
- *What’s the average daily billing amount for patients with Aetna coverage?*
- *How many patient reviews have been submitted from Florida?*
- *For visits that include a chief complaint, what percentage also have a review?*
- *What percentage of visits at each hospital include patient reviews?*
- *Which physician has received the highest number of reviews for their visits?*
- *What is the unique identifier for Dr. James Cooper?*
- *Show all reviews associated with visits handled by physician 270 — include every one.*
