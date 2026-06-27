from services.llm_provider import generate_response

from services.prompt_builder import (

    build_contents,

    build_system_instruction

)


def chat(

    conversation,

    memory=None,

    knowledge=None,

    profile=None,

    episode=None,

    reflection=None,

    mood=None

):

    system_instruction = build_system_instruction(

        memory,

        knowledge,

        profile,

        episode,

        reflection,

        mood

    )

    contents = build_contents(

        conversation

    )

    return generate_response(

        contents,

        system_instruction

    )