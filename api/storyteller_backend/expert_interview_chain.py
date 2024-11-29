# Standard libraries
from pydantic.v1 import BaseModel, Field
from typing import List, Any

# Langchain libraries
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.runnables import RunnableParallel


class Question(BaseModel):
    """Single Output - A question with no answer"""

    question: str = Field(
        None, description="An interview question to to clarify the story topic.")
    answer: None = None


class InterviewQuestions(BaseModel):
    """Output for Interview questions"""

    questions: List[Question] = Field(
        ..., min_items=5, max_items=5, description="List of questions to clarify the story topic."
    )


class InterviewChain:
    def __init__(self, topic: str, genre: str):
        self.topic = topic
        self.genre = genre
        self.llm = ChatOpenAI(temperature=0)

    def __call__(self) -> Any:
        # Create an LLM:
        model = ChatOpenAI(temperature=0.6)

        # Set up a parser + inject instructions into the prompt template:
        parser: PydanticOutputParser = PydanticOutputParser(
            pydantic_object=InterviewQuestions
        )

        system_message = """You are a story writer.
        You are now going to interview a content expert(user). You will ask them questions about the following topic: {topic} with genre {genre}.

        You must follow the following rules:
        - Return a list of questions that you would ask a content expert about the topic.
        - You must ask at least and at most 5 questions.
        - You must ask questions that are open-ended and not yes/no questions.
        - Identify whether the topic contains any characters name or settings/location.
        - If the topic already include the characters name or settings/location , you must skip the questions related to that,
        - However, if the topic does not include the characters name or settings/location, you must ask about that.
        - You can ask about the stories characters name
        - You can ask about the relationships between the characters
        - You can ask about the characters background
        - You can ask about the settings/location of the story
        - You can ask about the specific scene that the user want to include in the story
        - You can ask about the how the story gonna end

        {format_instructions}
        """

        system_prompt = SystemMessagePromptTemplate.from_template(
            system_message)
        human_prompt = HumanMessagePromptTemplate.from_template(
            """Give me the first 5 questions"""
        )

        # Create the prompt:
        prompt = ChatPromptTemplate.from_messages(
            [system_prompt, human_prompt])

        chain = (
            RunnableParallel(
                topic=lambda x: self.topic,
                genre=lambda x: self.genre,
                format_instructions=lambda x: parser.get_format_instructions(),
            )
            | prompt
            | model
        )

        # Run the chat:
        result = chain.invoke(
            {
                "topic": self.topic,
                "genre": self.genre,
                "format_instructions": parser.get_format_instructions(),
            }
        )

        # Parse the llm response::
        return parser.parse(result.content)
