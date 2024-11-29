from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from typing import Any
from pydantic.v1 import BaseModel


class StorySummary(BaseModel):
    summary: str


# Langchain libraries:

# Custom types:
load_dotenv()


class StorySummarizer:
    def __init__(self, story: str):
        self.story = story

        # Create a prompt
        prompt_content = """
            Summarize the following story into one concise summary.
            The summary should cover the key events and major points of the story without dividing it into chapters.

            Story: {story}
            ---
            Output format: {format_instructions}
        """

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            prompt_content
        )
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt])

        # Create an output parser
        self.parser = PydanticOutputParser(pydantic_object=StorySummary)

        # Set up the chain
        self.summarization_chain = self.chat_prompt | ChatOpenAI(
            temperature=0, model="gpt-4o") | self.parser

    def summarize_story(self) -> Any:
        print("Generating the Story Summary...\n---")
        result = self.summarization_chain.invoke(
            {
                "story": self.story,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        print("Finished generating the summary!\n---")
        return result
