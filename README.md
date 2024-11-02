# Run the project locally

```
docker compose up
```

# Current Scope
Priority
Text -> Image

Include Chapter and Remove Scene
1. Selection of Topic , Genre (Romantic ...) 
- Selection of Candidate of Topic
(Accuracy Topic based on the genre (EG: if possible to generate all the same topic based on genre, it consider high accuracy)
2. Generate Characters Description and Photo (Able to change the photo of characters)
3. Generate Table of Content
4. Generate Chapter
5. Generate Chapter Content

Metric(Image, Text)
- Prompt to Output
- Accuracy of Text Generation 

- Accuracy of Image Generation 
(List down the accuracy of generated image based on the prompt)
(May only limit to color , EG hair color, color of costume)

Limit (10 pages of stories)
- limit by number of words/stories
- limit number of characters

---

# Task to do (Archived)

0. Selection of Model (Add on other model, Fine-tune model, mistral-ai, Ollama)
  - Fine Tune Method
    1. PERT
    2. QLoRa
    3. RLHF
    4. DPO
2. Upload PDF <- Current Progess⭐
3. Commit point (time travel) (Priority: 1)
4. Q&A

- Ask any question about current generated stories
- locate commit certain commit point

4. Character Image Generation✅ -> ❗❗❗Futher Improvemnt: Generate in another tab and can export to png

- document chain (Summarize, map reduce)
- Dalle

5. Agent - tools (TavilySearch, Wikipedia...)
6. Optional - Callback (Count token to limit token usage, 1 people 100000 token)
7. Export PDF

- Update Memory Implementation to mongo db

Progress Result:

# Generate Stories
![image](https://github.com/user-attachments/assets/1d076280-1d05-4fa6-a380-f39a98939d14)


# Generate Character Image
![image](https://github.com/user-attachments/assets/b28f7066-4b43-4242-9f96-bc2aae4834cf)

