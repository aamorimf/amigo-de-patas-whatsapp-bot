from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.message_handler import process_incoming_message

router = APIRouter()


VERIFY_TOKEN = "DUMMY_TOKEN_AMIGOPATAS"


class IncomingMessage(BaseModel):
    phone: str
    text: str


class SimpleWebhookPayload(BaseModel):
    phone_number: str
    message: str


@router.get("/webhook")
async def verify_webhook(request: Request) -> int | dict[str, str]:
    """
    Simple webhook verification endpoint similar to Meta webhook verification.
    """
    mode = request.query_params.get("hub.mode")
    challenge = request.query_params.get("hub.challenge")
    verify_token = request.query_params.get("hub.verify_token")

    if mode == "subscribe" and verify_token == VERIFY_TOKEN and challenge:
        try:
            return int(challenge)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid challenge value.")

    raise HTTPException(status_code=403, detail="Verification failed.")


@router.post("/webhook")
async def handle_whatsapp_message(
    payload: SimpleWebhookPayload,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """
    Simplified webhook endpoint for local portfolio simulation.
    Expected payload:
    {
        "phone_number": "21999999999",
        "message": "oi"
    }
    """
    phone_number = payload.phone_number.strip()
    message_body = payload.message.strip()

    if not message_body:
        return {"status": "ignored", "message": "Empty message body."}

    try:
        response_text = process_incoming_message(db, phone_number, message_body)
        return {
            "status": "success",
            "reply_to": phone_number,
            "response": response_text,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/test-message")
async def test_message(
    payload: IncomingMessage,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """
    Manual testing endpoint for Swagger/Postman.
    Expected payload:
    {
        "phone": "21999999999",
        "text": "oi"
    }
    """
    phone_number = payload.phone.strip()
    message_body = payload.text.strip()

    if not message_body:
        return {"status": "ignored", "message": "Empty message body."}

    try:
        response_text = process_incoming_message(db, phone_number, message_body)
        return {
            "status": "success",
            "reply_to": phone_number,
            "response": response_text,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/webhook/twilio")
async def handle_twilio_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db),
):
    phone_number = From.strip()
    message_body = Body.strip()

    response_text = process_incoming_message(db, phone_number, message_body)

    twiml = MessagingResponse()
    twiml.message(response_text)

    return Response(
        content=str(twiml),
        media_type="application/xml",
    )