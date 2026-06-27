from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Message, Conversation
from auth_utils import get_current_user
from services.ai.orchestrator import AIOrchestrator

router = APIRouter()


class SendMessageRequest(BaseModel):

    conversation_id: int
    content: str


@router.post("/send")
def send_message(

    request: SendMessageRequest,

    db: Session = Depends(get_db),

    user=Depends(get_current_user)

):

    conversation = db.query(Conversation).filter(

        Conversation.id == request.conversation_id,

        Conversation.user_id == user["user_id"]

    ).first()

    if not conversation:

        raise HTTPException(

            status_code=404,

            detail="Conversation not found"

        )

    ##################################################
    # Save User Message
    ##################################################

    user_message = Message(

        conversation_id=request.conversation_id,

        role="user",

        content=request.content

    )

    db.add(user_message)

    db.commit()

    db.refresh(user_message)

    ##################################################
    # Load Conversation History
    ##################################################

    history = db.query(Message).filter(

        Message.conversation_id == request.conversation_id

    ).order_by(Message.id).all()

    conversation_messages = []

    for message in history:

        conversation_messages.append({

            "role": message.role,

            "content": message.content

        })

    ##################################################
    # AI Orchestrator
    ##################################################

    orchestrator = AIOrchestrator()
    print("========== ORCHESTRATOR ==========")
    print(orchestrator)
    print(orchestrator.__dict__)
    print("==================================")
    
    result = orchestrator.chat(

        db=db,

        user_id=user["user_id"],

        conversation=conversation_messages,

        latest_message=request.content,

        current_title=conversation.title

    )

    reply = result["reply"]

    new_title = result["title"]

    episode = result["episode"]

    ##################################################
    # Save Assistant Message
    ##################################################

    assistant_message = Message(

        conversation_id=request.conversation_id,

        role="assistant",

        content=reply

    )

    db.add(assistant_message)

    db.commit()

    db.refresh(assistant_message)

    ##################################################
    # Update Conversation Title
    ##################################################

    if new_title:

        conversation.title = new_title

        db.commit()

        db.refresh(conversation)

    ##################################################
    # Response
    ##################################################

    return {

        "user_message": {

            "id": user_message.id,

            "role": user_message.role,

            "content": user_message.content

        },

        "assistant_message": {

            "id": assistant_message.id,

            "role": assistant_message.role,

            "content": assistant_message.content

        },

        "conversation_title": conversation.title,

        "episode_id": episode.episode_id if episode else None

    }


@router.get("/{conversation_id}")
def get_messages(

    conversation_id: int,

    db: Session = Depends(get_db),

    user=Depends(get_current_user)

):

    conversation = db.query(Conversation).filter(

        Conversation.id == conversation_id,

        Conversation.user_id == user["user_id"]

    ).first()

    if not conversation:

        raise HTTPException(

            status_code=404,

            detail="Conversation not found"

        )

    messages = db.query(Message).filter(

        Message.conversation_id == conversation_id

    ).order_by(Message.id).all()

    return messages