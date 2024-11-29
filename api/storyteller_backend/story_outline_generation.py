from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from typing import List, Any
from pydantic.v1 import BaseModel


class Chapter(BaseModel):
    chapter_number: int
    chapter_title: str


class StoriesOutline(BaseModel):
    chapters: List[Chapter]


# Langchain libraries:

# Custom types:
load_dotenv()


class StoryOutlineGenerator:
    def __init__(self, input: str, genre: str, interview_questions_and_answers: Any):
        self.input = input
        self.genre = genre
        self.interview_questions_and_answers = interview_questions_and_answers

        # Create a prompt
        prompt_content = """
            Based on the user_queries and genre and the interview answer, generate only 3 chapters for the stories
            user_queries: {input}
            genre: {genre}
            ---
            Here is the interview which I answered: {interview_questions_and_answers}
            - If the interview question do not contain the answers, it is consider user let you to decide the answer
            ---
            Output format: {format_instructions}
            """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            prompt_content
        )
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt])

        # Create an output parser
        self.parser = PydanticOutputParser(pydantic_object=StoriesOutline)

        # Set up the chain
        self.outline_chain = self.chat_prompt | ChatOpenAI(
            temperature=0, model="gpt-4o") | self.parser

    def generate_outline(self) -> Any:
        print("Generating the Stories Outline...\n---")
        result = self.outline_chain.invoke(
            {
                "input": self.input,
                "genre": self.genre,
                "interview_questions_and_answers": self.interview_questions_and_answers,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        print("Finished generating the outline!\n---")
        return result
