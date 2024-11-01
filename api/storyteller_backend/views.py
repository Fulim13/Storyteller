from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, ConfigurableField
from dotenv import load_dotenv
from langchain_core.prompts.chat import ChatPromptTemplate
import json
from operator import itemgetter
from openai import OpenAI
# from PyPDF2 import PdfReader
import os

load_dotenv()
# memory = ConversationSummaryMemory(llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"))
# memory = ConversationBufferMemory()

@api_view(['POST'])
def send_some_data(request):

    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo").configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="gpt-3.5-turbo",
    gpt4=ChatOpenAI(temperature=0, model="gpt-4").configurable_fields(
        temperature=ConfigurableField(
            id="temperature",
            name="LLM Temperature",
            description="The temperature of the LLM",
        )
    )).configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
        )
    )

    # Extract message and genre from the request
    input_message = request.data.get('message', '')
    genre = request.data.get('genre', 'Fantasy')  # Default to 'Fantasy' if not provided
    user_input = request.data.get('message', '')
    temperature = request.data.get('temperature', 0.0)
    llm = request.data.get('model', 'gpt-3.5-turbo')

    # Load previous memory
    # previous_context = str(memory.load_memory_variables({}))

    # If needed memory, you can set this prompt
    #   Here is the context from our previous conversation:
    # {previous_context}

    # Create the subchains:
    character_generation_prompt = ChatPromptTemplate.from_template(
        """
    I want you to brainstorm 2 characters for my short story. The
    genre is {genre}. Each character must have a Name and a Biography.
    You must provide a name and biography for each character, this is very
    important!

    Additional User Input(Context):
    {user_input}
    ---
    Example response:
    Name: CharWiz, Biography: A wizard who is a master of magic.
    Name: CharWar, Biography: A warrior who is a master of the sword.
    ---
    Characters: """
    )

    plot_generation_prompt = ChatPromptTemplate.from_template(
        """

    Given the following characters and the genre, create an effective
    plot for a short story:
    Additional User Input(Context):
    {user_input}
    Characters:
    {characters}
    ---
    Genre: {genre}
    ---
    Plot: """
    )

    scene_generation_plot_prompt = ChatPromptTemplate.from_template(
        """
    Act as an effective content creator.
    Given multiple characters and a plot, you are responsible for
    generating the various scenes for each act.
    You must decompose the plot into multiple effective scenes:
    Additional User Input(Context):
    {user_input}
    ---
    Characters:
    {characters}
    ---
    Genre: {genre}
    ---
    Plot: {plot}
    ---
    Example response:
    Scenes:
    Scene 1: Some text here.
    Scene 2: Some text here.
    Scene 3: Some text here.
    ----
    Scenes:
    """
    )

    character_generation_chain = (character_generation_prompt
                                | model
                                | StrOutputParser())
    plot_generation_chain = (plot_generation_prompt
                           | model
                           | StrOutputParser())
    scene_generation_plot_chain = (scene_generation_plot_prompt
                                 | model
                                 | StrOutputParser())
    master_chain = ({
        "characters": character_generation_chain,
        "genre": RunnablePassthrough(),
        "user_input": RunnablePassthrough(),
        # "previous_context": RunnablePassthrough()
        }
        | RunnableParallel(
        characters=itemgetter("characters"),
        user_input=itemgetter("user_input"),
        genre=itemgetter("genre"),
        # previous_context=itemgetter("previous_context"),
        plot=plot_generation_chain,  # Generate plot based on characters and genre
        ) | RunnableParallel(
        characters=itemgetter("characters"),
        genre=itemgetter("genre"),
        user_input=itemgetter("user_input"),
        # previous_context=itemgetter("previous_context"),
        plot=itemgetter("plot"),
        scenes=scene_generation_plot_chain,  # Generate scenes based on characters, plot, and genre
        )
    ).with_config(
        temperature=temperature,
        llm=llm
    )
    print(user_input)

    story_result = master_chain.invoke({
        "genre": genre,
        "user_input": user_input,
        # "previous_context": previous_context
        })

    print(story_result)

     # Ensure the output is a string
    # story_result_str = json.dumps(story_result) if isinstance(story_result, (dict, list)) else str(story_result)

    # Save the new context to memory
    # memory.save_context({"input": input_message}, {"output": story_result_str})

    return Response({
        "data": story_result
    })

@api_view(['POST'])
def generate_character_image(request):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    name = request.data.get('name', '')
    biography = request.data.get('biography', '')
    genre = request.data.get('genre', '')

    # Create a detailed prompt for DALL-E
    prompt = f"A character portrait in {genre} style. The character is {name}, who is {biography}. The image should be detailed and high quality, showing the character's distinctive features and personality."

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        return Response({
            "success": True,
            "image_url": image_url
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)


# @api_view(['POST'])
# def upload_pdf(request):
#     pdf_file = request.FILES['pdf_file']

#     # Save the uploaded PDF file to the 'uploads' directory
#     with open(f'uploads/{pdf_file.name}', 'wb+') as destination:
#         for chunk in pdf_file.chunks():
#             destination.write(chunk)



#     return Response({
#         "data": pdf_content
#     })
# INstaed of saving the pdf file to the uploads directory, we can extract the text from the pdf file and return it as a response
