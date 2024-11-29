from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from typing import List, Any
from pydantic.v1 import BaseModel


class TitleCandidates(BaseModel):
    titles: List[str]


# Langchain libraries:

# Custom types:
load_dotenv()


class TitleGenerator:
    def __init__(self, summary: str):
        self.summary = summary

        # Create a prompt
        prompt_content = """
            Based on the following summary of the story, generate a list of 5 potential title candidates.
            The titles should reflect the key themes and essence of the story.

            Summary: {summary}
            ---
            Output format: {format_instructions}
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            prompt_content
        )
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt])

        # Create an output parser
        self.parser = PydanticOutputParser(pydantic_object=TitleCandidates)

        # Set up the chain
        self.title_chain = self.chat_prompt | ChatOpenAI(
            temperature=0, model="gpt-4o") | self.parser

    def generate_titles(self) -> Any:
        print("Generating potential titles for the story...\n---")
        result = self.title_chain.invoke(
            {
                "summary": self.summary,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        print("Finished generating the title candidates!\n---")
        return result
