# Setup For Ollama

1. Create a new virtual environment `python -m venv story-teller`
2. Install the requirements `pip install -r requirements.txt`
3. Install Ollama from Ollama's official repository [Download Link](https://github.com/ollama/ollama)
4. Run `ollama pull llama3` to download the model
5. Run `ollama serve` to start the server
6. Run the create_database.py file to create the database
7. Run the app.py file to ask question `python app.py <question>`

# Setup For Open AI

1. Create a new virtual environment `python -m venv story-teller`
2. Install the requirements `pip install -r requirements.txt`
3. Create .env file and add the following variables

```
OPENAI_API_KEY=your_secret_key
```

4. Go to get_llm.py and uncomment the OpenAI line and comment the Ollama Line
5. Run the create_database.py file to create the database
6. Run the app.py file to ask question `python app.py <question>`

# Example Question can ask:

1. How does Alice meet the Mad Hatter?
2. What happens when Alice first falls down the rabbit hole?
3. Describe the tea party scene with the Mad Hatter and the March Hare.

